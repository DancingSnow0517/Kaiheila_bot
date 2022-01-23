import asyncio
import traceback
from datetime import datetime, timedelta

from khl import Bot
from khl.task.manager import log

from ..browser import get_dynamic_screenshot
from ..config import Config
from ..libs.bilireq import BiliReq
from ..libs.dynamic import Dynamic

last_time: dict = {}


async def dy_pusher(bot: Bot, config: Config):
    """动态推送"""
    log.info('动态推送头')
    uid = config.getnext_subscription_uid()
    if uid is None:
        return
    print(uid)
    user = config.get_subscription(uid)
    name = user.name

    log.debug(f'爬取动态 {name}（{uid}）')
    br = BiliReq()

    dynamics = (await br.get_user_dynamics(uid)).get('cards', [])

    if len(dynamics) == 0:
        return

    if uid not in last_time:
        dynamic = Dynamic(dynamics[0])
        last_time[uid] = dynamic.time
        return

    for dynamic in dynamics[4::-1]:
        dynamic = Dynamic(dynamic)
        if dynamic.time > last_time[uid] and dynamic.time > datetime.now().timestamp() - timedelta(minutes=10).seconds:
            log.info(f'检测到新动态（{dynamic.id}）：{name}（{uid}）')
            image = None
            for _ in range(3):
                try:
                    image = await get_dynamic_screenshot(dynamic.url)
                    break
                except Exception as e:
                    log.error('截图失败，以下为错误日志:')
                    log.error(traceback(e))
                await asyncio.sleep(0.1)
            if not image:
                log.error('已达到重试上限，将在下个轮询中重新尝试')
            await dynamic.format(image, bot)
            guild = await bot.fetch_guild(config.khl_server_id)
            channels = await guild.fetch_channel_list()
            for i in channels:
                if i.id in config.khl_channel:
                    await i.send([dynamic.msg_card.build()])

            last_time[uid] = dynamic.time
