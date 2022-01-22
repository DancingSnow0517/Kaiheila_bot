import logging

from khl import Bot

from utils import commands
from utils.config import Config

help_msg = '''[!!help] 显示帮助信息
[!!mc] 发送消息到游戏
[!!reload] 重新加载配置文件'''

config: Config

if __name__ == '__main__':
    logging.basicConfig(level='INFO', format='[%(asctime)s] [%(threadName)s/%(levelname)s]: %(message)s')

    config = Config.load()
    khl_bot = Bot(token=config.token)

    commands.register(khl_bot, config.prefixes, config)

    khl_bot.run()
