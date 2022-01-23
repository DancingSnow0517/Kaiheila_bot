import logging

from khl import Bot

from utils import commands
from utils.browser import delete_pyppeteer, install
from utils.config import Config
from utils.pusher.dynamic_pusher import dy_pusher
from utils.pusher.live_pusher import live_pusher

help_msg = '''[!!help] 显示帮助信息
[!!mc] 发送消息到游戏
[!!reload] 重新加载配置文件'''

config: Config

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG', format='[%(asctime)s] [%(threadName)s/%(levelname)s]: %(message)s')

    config = Config.load()

    khl_bot = Bot(token=config.token)
    commands.register(khl_bot, config.prefixes, config)

    # Chromium 相关
    delete_pyppeteer(config)
    install()

    @khl_bot.task.add_interval(seconds=10, timezone='Asia/Shanghai')
    async def push():
        await dy_pusher(khl_bot, config)
        await live_pusher(khl_bot, config)

    # 计划任务
    # scheduler = BackgroundScheduler()
    # intervalTrigger = IntervalTrigger(seconds=10)
    # scheduler.add_job(dy_pusher, intervalTrigger, id='dy_pusher', args=[khl_bot])
    # scheduler.start()

    khl_bot.run()
