import json
import os

from khl import Bot, Message, MessageTypes
from khl_card.card import *
from khl_card.modules import *
from khl_card.accessory import *
from mcdreforged.minecraft.rcon.rcon_connection import RconConnection

from .config import Config
from .libs.bilireq import BiliReq, RequestError
from .libs.player_list import get_server_player_list

help_msg = '''[!!help] 显示帮助信息
[!!list] 查看服务器玩家列表
[!!stats] 查看统计信息帮助
[!!whitelist] 查看白名单相关帮助
[!!addRcon] 添加rcon服务器'''

Bilibili_bot_msg = '''[!!关注] <UID>
[!!取关] <UID>
[!!关注列表] 
[!!开启动态] <UID>
[!!关闭动态] <UID>
[!!开启直播] <UID>
[!!关闭直播] <UID>
[!!关闭权限] 关闭后所有人能叫出机器人
[!!开启权限] 开启后需要权限，才能叫出机器人'''

stats_help_msg = '''[!!stats] <类别> <内容>
`<类别>`: `killed`, `killed_by`, `dropped`, `picked_up`, `used`, `mined`, `broken`, `crafted`, `custom`, `plugin`
更多详情见[Wiki](https://minecraft.fandom.com/zh/wiki/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF)
例子：
`!!stats used diamond_pickaxe`
`!!stats custom time_since_rest`'''

whitelist_help_msg = '''[!!whitelist] add <name> 添加白名单
[!!whitelist] remove <name> 删除白名单'''

c1_list = [
    'killed',
    'killed_by',
    'dropped',
    'picked_up',
    'used',
    'mined',
    'broken',
    'crafted',
    'custom',
    'plugin'
]
plugin_list = [
    'digT',
    'active'
]
tool_list = [
    'wooden_pickaxe',
    'wooden_axe',
    'wooden_shovel',
    'wooden_hoe',
    'stone_pickaxe',
    'stone_axe',
    'stone_shovel',
    'stone_hoe',
    'iron_pickaxe',
    'iron_axe',
    'iron_shovel',
    'iron_hoe',
    'gold_pickaxe',
    'gold_axe',
    'gold_shovel',
    'gold_hoe',
    'diamond_pickaxe',
    'diamond_axe',
    'diamond_shovel',
    'diamond_hoe',
    'netherite_pickaxe',
    'netherite_axe',
    'netherite_shovel',
    'netherite_hoe'
]


def register(bot: Bot, prefixes, config: Config):
    @bot.command(name='help', prefixes=prefixes)
    async def print_helpmsg(msg: Message):
        help_card = Card(
            [
                Header('帮助信息'),
                Section(Kmarkdown(f'```\n{help_msg}\n```')),
                Divider(),
                Header('Bilibili机器人帮助信息'),
                Section(Kmarkdown(f'```\n{Bilibili_bot_msg}\n```'))
            ]
        )
        await msg.reply([help_card.build()])

    @bot.command(aliases=['关注'], prefixes=prefixes)
    async def sub(msg: Message, uid: str = ''):
        global name
        if config.bilibili_permission:
            if msg.author.id not in config.permission:
                await msg.reply('你没有权限执行')
                return
        if uid == '':
            await msg.reply('请输入要关注的UID')
            return
        if not uid.isdecimal():
            await msg.reply('UID 必须为纯数字')
            return
        up = config.get_subscription(uid)
        if up is None:
            br = BiliReq()
            try:
                name = (await br.get_info(uid))['name']
            except RequestError as e:
                if e.code == -400 or e.code == -404:
                    await msg.reply('UID不存在，注意UID不是房间号')
                elif e.code == -412:
                    await msg.reply('操作过于频繁IP暂时被风控，请半小时后再尝试')
                else:
                    err_card = Card([
                        Header('未知错误, 请联系开发者反馈'),
                        Section(Kmarkdown(f'```\n{str(e)}\n```'))
                    ])
                    await msg.reply([err_card.build()])
        result = config.add_subscription(uid, name=name)
        if result:
            await msg.reply(f'已关注 {name}（{uid}）')
        else:
            await msg.reply(f'{name}（{uid}）已经关注了')

    @bot.command(aliases=['取关'], prefixes=prefixes)
    async def del_sub(msg: Message, uid: str = ''):
        if config.bilibili_permission:
            if msg.author.id not in config.permission:
                await msg.reply('你没有权限执行')
                return
        if uid == '':
            await msg.reply('请输入要关注的UID')
            return
        if not uid.isdecimal():
            await msg.reply('UID 必须为纯数字')
            return
        name = config.subscription[uid].name
        result = config.del_subscription(uid)
        if result:
            await msg.reply(f'已取关 {name}（{uid}）')
        else:
            await msg.reply(f'UID（{uid}）未关注')

    @bot.command(name='sub_list', aliases=['关注列表'], prefixes=prefixes)
    async def sub_list(msg: Message):
        names = '**名字**\n'
        stats = '**直播 | 动态**\n'
        for i in config.subscription:
            t = config.get_subscription(i)
            names += f'{t.name}({i})\n'
            stats += f'{"开" if t.live else "关"}    |    {"开" if t.dynamic else "关"}\n'
        list_card = Card([
            Header('关注列表'),
            Section(Paragraph(2, [
                Kmarkdown(names),
                Kmarkdown(stats)
            ]))
        ])
        await msg.reply([list_card.build()])

    @bot.command(aliases=['开启动态'], prefixes=prefixes)
    async def dy_on(msg: Message, uid: str):
        if config.bilibili_permission:
            if msg.author.id not in config.permission:
                await msg.reply('你没有权限执行')
                return
        if uid == '':
            await msg.reply('请输入要关注的UID')
            return
        if not uid.isdecimal():
            await msg.reply('UID 必须为纯数字')
            return

        if uid not in config.subscription:
            await msg.reply(f'UID（{uid}）未关注，请先关注后再操作')
        else:
            name = config.subscription[uid].name
            config.subscription[uid].dynamic = True
            config.save()
            await msg.reply(f'已开启 {name}（{uid}）的动态推送')

    @bot.command(aliases=['关闭动态'], prefixes=prefixes)
    async def dy_off(msg: Message, uid: str):
        if config.bilibili_permission:
            if msg.author.id not in config.permission:
                await msg.reply('你没有权限执行')
                return
        if uid == '':
            await msg.reply('请输入要关注的UID')
            return
        if not uid.isdecimal():
            await msg.reply('UID 必须为纯数字')
            return

        if uid not in config.subscription:
            await msg.reply(f'UID（{uid}）未关注，请先关注后再操作')
        else:
            name = config.subscription[uid].name
            config.subscription[uid].live = False
            config.save()
            await msg.reply(f'已关闭 {name}（{uid}）的动态推送')

    @bot.command(aliases=['开启直播'], prefixes=prefixes)
    async def live_on(msg: Message, uid: str):
        if config.bilibili_permission:
            if msg.author.id not in config.permission:
                await msg.reply('你没有权限执行')
                return
        if uid == '':
            await msg.reply('请输入要关注的UID')
            return
        if not uid.isdecimal():
            await msg.reply('UID 必须为纯数字')
            return

        if uid not in config.subscription:
            await msg.reply(f'UID（{uid}）未关注，请先关注后再操作')
        else:
            name = config.subscription[uid].name
            config.subscription[uid].live = True
            config.save()
            await msg.reply(f'已开启 {name}（{uid}）的直播动态推送')

    @bot.command(aliases=['关闭直播'], prefixes=prefixes)
    async def live_off(msg: Message, uid: str):
        if config.bilibili_permission:
            if msg.author.id not in config.permission:
                await msg.reply('你没有权限执行')
                return
        if uid == '':
            await msg.reply('请输入要关注的UID')
            return
        if not uid.isdecimal():
            await msg.reply('UID 必须为纯数字')
            return

        if uid not in config.subscription:
            await msg.reply(f'UID（{uid}）未关注，请先关注后再操作')
        else:
            name = config.subscription[uid].name
            config.subscription[uid].live = False
            config.save()
            await msg.reply(f'已关闭 {name}（{uid}）的直播动态推送')

    @bot.command(aliases=['开启权限'], prefixes=prefixes)
    async def perm_on(msg: Message):
        if msg.author.id not in config.permission:
            await msg.reply('你没有权限执行')
            return
        config.bilibili_permission = True
        config.save()
        await msg.reply('权限已经开启了，只有管理员可以操作')

    @bot.command(aliases=['关闭权限'], prefixes=prefixes)
    async def perm_off(msg: Message):
        if msg.author.id not in config.permission:
            await msg.reply('你没有权限执行')
            return
        config.bilibili_permission = False
        config.save()
        await msg.reply('权限已经关闭了，所有人均可操作')

    @bot.command(prefixes=prefixes)
    async def stats(msg: Message, *args):
        stats_card = Card([
            Header('stats 帮助信息'),
            Section(Kmarkdown(stats_help_msg))
        ])
        if len(args) < 2:
            await msg.reply([stats_card.build()])
            return
        if args[0] not in c1_list:
            await msg.reply([stats_card.build()])
            return
        # stats文件夹列表
        stats_path = config.mcdr_server_path + '/server/world/stats'
        # 利用StatsHelper获取的uuid列表
        uuid_file = config.mcdr_server_path + '/config/StatsHelper/uuid.json'
        with open(uuid_file, 'r', encoding='utf-8') as f:
            uuid = json.load(f)
        data = {}
        if args[0] != 'plugin':
            for i in uuid:
                if not os.path.exists(f'{stats_path}/{uuid[i]}.json'):
                    continue
                with open(f'{stats_path}/{uuid[i]}.json', 'r', encoding='utf-8') as f:
                    js = json.load(f)
                player_data = js['stats']
                if f'minecraft:{args[0]}' in player_data:
                    if f'minecraft:{args[1]}' in player_data[f'minecraft:{args[0]}']:
                        data[i] = player_data[f'minecraft:{args[0]}'][f'minecraft:{args[1]}']
        else:
            if args[1] not in plugin_list:
                await msg.reply('`plugin` 中目前支持 `digT`和`active`', type=MessageTypes.KMD)
                return
            if args[1] == 'digT':
                for i in uuid:
                    data[i] = 0
                    if not os.path.exists(f'{stats_path}/{uuid[i]}.json'):
                        continue
                    with open(f'{stats_path}/{uuid[i]}.json', 'r', encoding='utf-8') as f:
                        js = json.load(f)
                    player_data = js['stats']
                    for tool in tool_list:
                        if 'minecraft:used' in player_data:
                            if f'minecraft:{tool}' in player_data['minecraft:used']:
                                data[i] += int(player_data['minecraft:used'][f'minecraft:{tool}'])
            if args[1] == 'active':
                for i in uuid:
                    if not os.path.exists(f'{stats_path}/{uuid[i]}.json'):
                        continue
                    with open(f'{stats_path}/{uuid[i]}.json', 'r', encoding='utf-8') as f:
                        js = json.load(f)
                    player_data = js['stats']
                    if 'minecraft:custom' in player_data:
                        if 'minecraft:play_time' in player_data['minecraft:custom']:
                            data[i] = round(player_data['minecraft:custom']['minecraft:play_time'] / 20 / 60 / 60, 2)

        if data == {}:
            await msg.reply('未知或空统计信息')
        else:
            sorted_data = sorted(data.items(), key=lambda kv: kv[1], reverse=True)
            count = 0
            ranks = '**排名**\n'
            players = '**玩家**\n'
            values = '**值**\n'
            for i in sorted_data:
                count += 1
                if count == 15:
                    ranks += f'#{count}'
                    players += f'{i[0]}'
                    values += f'{i[1]}' if i[1] < 1000 else f'{format(i[1] / 1000, ".3f")}'
                    break
                else:
                    ranks += f'#{count}\n'
                    players += f'{i[0]}\n'
                    values += f'{i[1]}\n' if i[1] < 1000 else f'{format(i[1] / 1000, ".3f")}K\n'
            data_card = Card([
                Header(f'统计信息 {args[0]}.{args[1]}'),
                Section(Paragraph(3, [Kmarkdown(ranks), Kmarkdown(players), Kmarkdown(values)]))
            ])
            await msg.reply([data_card.build()])

    @bot.command(prefixes=prefixes, aliases=['list'])
    async def player_list(msg: Message):
        rcon_list = config.get_rcon_list()
        data = {}
        online_total = 0
        for i in rcon_list:
            data[i.name] = {}
            rcon = RconConnection(address=i.address, password=i.password, port=i.port)
            try:
                rcon.connect()
                rt = rcon.send_command('list')
                rcon.disconnect()
                data[i.name]['amount'], data[i.name]['limit'], data[i.name]['players'] = get_server_player_list(rt)
                online_total += data[i.name]['amount']
            except ConnectionRefusedError:
                data[i.name] = ''
        list_card = Card([
            Header(f'共有 {online_total} 名玩家已连接至此服务器。')
        ])
        for i in config.rcon:
            list_card.modules.append(Section(Kmarkdown(f'**{i.name}: **')))
            if data[i.name] == '':
                list_card.modules.append(Section(Kmarkdown(f'```\n服务器未连接\n```')))
            else:
                list_card.modules.append(Section(Kmarkdown(f'```\n{data[i.name]["players"]}\n```')))
        await msg.reply([list_card.build()])

    @bot.command(prefixes=prefixes)
    async def addRcon(msg: Message, *args):
        if msg.author.id not in config.permission:
            await msg.reply('你没有权限执行')
            return
        if len(args) != 4:
            await msg.reply('用!!addRcon <name> <address> <password> <port>')
            return
        config.add_rcon(name=args[0], address=args[1], password=args[2], port=int(args[3]))
        await msg.reply(f'RCON {args[0]} 添加成功')

    @bot.command(prefixes=prefixes)
    async def whitelist(msg: Message, *args):
        if msg.author.id not in config.permission:
            await msg.reply('你没有权限执行')
            return
        if len(args) != 2:
            await msg.reply(f'```\n{whitelist_help_msg}\n```', type=9)
            return
        if args[0] == 'add':
            proxy = config.get_velocity_rcon()
            rcon = RconConnection(address=proxy.address, port=proxy.port, password=proxy.password)
            rcon.connect()
            rcon.send_command(f'lls_whitelist add {args[1]} all -c')
            rcon.disconnect()
            await msg.reply(f'{args[1]} 白名添加成功')
            return
        if args[0] == 'remove':
            proxy = config.get_velocity_rcon()
            rcon = RconConnection(address=proxy.address, port=proxy.port, password=proxy.password)
            rcon.connect()
            rcon.send_command(f'lls_whitelist remove {args[1]} all')
            rcon.disconnect()
            await msg.reply(f'{args[1]} 白名删除成功')
            return
        await msg.reply(f'```\n{whitelist_help_msg}\n```', type=9)
