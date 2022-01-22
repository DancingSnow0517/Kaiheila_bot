from khl import Bot, Message
from khl_card.card import *
from khl_card.modules import *
from khl_card.accessory import *

from .config import Config
from .libs.bilireq import BiliReq, RequestError

help_msg = '''[!!help] 显示帮助信息
[!!mc] 发送消息到游戏'''

Bilibili_bot_msg = '''[!!关注] <UID>
[!!取关] <UID>
[!!关注列表] 
[!!开启动态] <UID>
[!!关闭动态] <UID>
[!!开启直播] <UID>
[!!关闭直播] <UID>
[!!关闭权限] 关闭后所有人能叫出机器人
[!!开启权限] 开启后需要权限，才能叫出机器人'''


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
    async def sub(msg: Message, uid: str):
        global name
        if config.bilibili_permission:
            if msg.author.id not in config.permission:
                await msg.reply('你没有权限执行')
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
        print(f'uid: {uid}, name: {name}')
        result = config.add_subscription(uid, name)
        if result:
            await msg.reply(f'已关注 {name}（{uid}）')
        else:
            await msg.reply(f'{name}（{uid}）已经关注了')
        # await msg.reply(f'正在关注 {uid}')
