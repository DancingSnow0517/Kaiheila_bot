import json

from khl import Bot, Message
import logging

from utils.card.card import Card
from utils.card.modules import *
from utils.card.accessory.text import *


def get_token() -> str:
    with open('TOKEN', 'r') as f:
        return f.read()


if __name__ == '__main__':
    card = Card(
        [
            header('测试卡片'),
            section(paragraph(3, [
                kmarkdown('**Repo**\ngithub.com'),
                kmarkdown('**Branch/Tag**\nmain'),
                kmarkdown('**Pusher**\ndddd')
            ]), 'right', image('https://avatars.githubusercontent.com/u/72912429', size='sm')),
            divider(),
            header('Commits'),
            section(paragraph(2, [
                kmarkdown('**Commits Hash**\n[abcdabcd](github.com)'),
                kmarkdown('**Message**\nfix markdown (#97)')
            ]))
        ]
    )
    khl_bot = Bot(token=get_token())
    logging.basicConfig(level='INFO')

    @khl_bot.command(name='hello', prefixes=['!!', '！！'])
    async def world(msg: Message):
        await msg.reply('world')

    @khl_bot.command(name='test', prefixes=['!!', '！！'])
    async def test(msg: Message):
        await msg.reply([card.build()])

    khl_bot.run()