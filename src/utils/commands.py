import json
import os

from khl import Bot, Message
from khl_card.card import *
from khl_card.modules import *
from khl_card.accessory import *

from .config import Config
from .libs.bilireq import BiliReq, RequestError

help_msg = '''[!!help] 显示帮助信息
[!!mc] 发送消息到游戏
[!!stats] 查看统计信息帮助'''

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
        result = config.add_subscription(uid, name)
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
        name = config.subscription[uid]['name']
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
            name = config.subscription[uid]['name']
            config.subscription[uid]['dynamic'] = True
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
            name = config.subscription[uid]['name']
            config.subscription[uid]['dynamic'] = False
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
            name = config.subscription[uid]['name']
            config.subscription[uid]['live'] = True
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
            name = config.subscription[uid]['name']
            config.subscription[uid]['live'] = False
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
        for i in uuid:
            if not os.path.exists(f'{stats_path}/{uuid[i]}.json'):
                continue
            with open(f'{stats_path}/{uuid[i]}.json', 'r', encoding='utf-8') as f:
                js = json.load(f)
            player_data = js['stats']
            if f'minecraft:{args[0]}' in player_data:
                if f'minecraft:{args[1]}' in player_data[f'minecraft:{args[0]}']:
                    data[i] = player_data[f'minecraft:{args[0]}'][f'minecraft:{args[1]}']
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
                    values += f'{i[1]}' if i[1] < 1000 else f'{format(i[1]/1000, ".3f")}'
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
