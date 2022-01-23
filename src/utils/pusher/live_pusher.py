from khl import Bot
from khl.task.manager import log
from khl_card.card import Card
from khl_card.modules import *
from khl_card.accessory import *

from ..config import Config
from ..libs.bilireq import BiliReq

status = {}


async def live_pusher(bot: Bot, config: Config):
    """直播推送"""

    uids = config.get_live_uid_list()

    if not uids:
        return
    log.debug(f'爬取直播列表，目前开播{sum(status.values())}人，总共{len(uids)}人')
    br = BiliReq()
    res = await br.get_live_list(uids)
    if not res:
        return

    for uid, info in res.items():
        new_status = 0 if info['live_status'] == 2 else info['live_status']
        if uid not in status:
            status[uid] = new_status
            continue
        old_status = status[uid]

        if new_status != old_status:
            room_id = info['short_id'] if info['short_id'] else info['room_id']
            url = 'https://live.bilibili.com/' + str(room_id)
            name = info['uname']
            title = info['title']
            cover = (info['cover_from_user'] if info['cover_from_user'] else info['keyframe'])
            log.info(f"检测到开播：{name}（{uid}）")
            live_msg = Card([
                Header(f'{name} 正在直播：'),
                Section(Kmarkdown(title), accessory=Image(cover, size='sm')),
                Section(Kmarkdown(f'[网页链接]({url})'))
            ])

            guild = await bot.fetch_guild(config.khl_server_id)
            channels = await guild.fetch_channel_list()
            for i in channels:
                if i.id in config.khl_channel:
                    await i.send([live_msg.build()])
        status[uid] = new_status
