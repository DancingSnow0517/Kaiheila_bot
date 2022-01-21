import json

from khl import Bot, Message
import logging

from utils.card.card import Card
from utils.card.modules import *


def get_token() -> str:
    with open('TOKEN', 'r') as f:
        return f.read()


if __name__ == '__main__':
    card = Card([header('测试卡片')])
    print(json.dumps([card.build()]))
    khl_bot = Bot(token=get_token())
    logging.basicConfig(level='INFO')

    @khl_bot.command(name='hello', prefixes=['!!', '！！'])
    async def world(msg: Message):
        await msg.reply('world')

    @khl_bot.command(name='test', prefixes=['!!', '！！'])
    async def test(msg: Message):
        await msg.reply([card.build()])

    khl_bot.run()