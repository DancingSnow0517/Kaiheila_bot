import functools
import inspect
import logging

import nest_asyncio
from khl import Bot, MessageTypes, Message
import colorama

from utils import commands
from utils.browser import delete_pyppeteer, install
from utils.cb_client import KaiheilaClient
from utils.config import Config, SentryConfig
from utils.libs.chatbridge.common.logger import Logger
from utils.pusher.dynamic_pusher import dy_pusher
from utils.pusher.live_pusher import live_pusher
from utils.libs.sentry import init_sentry

help_msg = '''[!!help] 显示帮助信息
[!!mc] 发送消息到游戏
[!!reload] 重新加载配置文件'''


class KaiheilaBot(Bot):
    def __init__(self, config: Config, sentry_config: SentryConfig):
        colorama.init(autoreset=True, wrap=True)
        init_sentry(sentry_config, config.log_level)
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
        if message.ctx.channel.id == self.config.khl_channel_mc_chat:
            self.cb_client.send_chat(message.content, message.author.nickname)


if __name__ == '__main__':
    nest_asyncio.apply()
    bot = KaiheilaBot(Config.load(), SentryConfig.load())
    bot.run()
