import collections
import logging
import functools
import inspect
import queue

from khl import Bot, MessageTypes, Message

from utils import commands
from utils.browser import delete_pyppeteer, install
from utils.config import Config
from utils.pusher.dynamic_pusher import dy_pusher
from utils.pusher.live_pusher import live_pusher
from utils.libs.chatbridge.common.logger import Logger
from utils.cb_client import KaiheilaClient

help_msg = '''[!!help] 显示帮助信息
[!!mc] 发送消息到游戏
[!!reload] 重新加载配置文件'''


class KaiheilaBot(Bot):
    def __init__(self, config: Config):
        self.patch_logging()
        super().__init__(config.token)
        self.config = config
        self.cb_client = KaiheilaClient(self)
        self.cb_client.start()
        self.client.register(MessageTypes.TEXT, self.on_text_msg)
        logging.basicConfig(level=config.log_level, format='[%(asctime)s] [%(module)s] [%(threadName)s/%(levelname)s]: %(message)s')
        commands.register(self, config.prefixes, config)

        # Chromium 相关
        delete_pyppeteer(config)
        install()

        self.task.add_interval(seconds=10, timezone='Asia/Shanghai')(self.push)

    @staticmethod
    def patch_logging():
        @functools.wraps(logging.getLogger)
        def proxyGetLogger(name: str):
            return Logger(name)

        proxyGetLogger.__signature__ = inspect.signature(logging.getLogger)
        logging.getLogger = proxyGetLogger

    async def push(self):
        await dy_pusher(self, self.config)
        await live_pusher(self, self.config)

    async def on_text_msg(self, message: Message):
        self.cb_client.send_chat(message.content, message.author.nickname)


if __name__ == '__main__':
    bot = KaiheilaBot(Config.load())
    bot.run()
