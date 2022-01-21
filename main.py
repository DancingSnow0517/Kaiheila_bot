import logging

from khl import Bot, Message

from utils.card.accessory.text import *
from utils.card.card import Card
from utils.card.modules import *


def get_token() -> str:
    with open('TOKEN', 'r') as f:
        return f.read()


if __name__ == '__main__':
    card = Card(
        [
            Header('测试卡片'),
            Section(Paragraph(3, [
                Kmarkdown('**Repo**\ngithub.com'),
                Kmarkdown('**Branch/Tag**\nmain'),
                Kmarkdown('**Pusher**\ndddd')
            ]), 'right', Image('https://avatars.githubusercontent.com/u/72912429', size='sm')),
            Divider(),
            Header('Commits'),
            Section(Paragraph(2, [
                Kmarkdown('**Commits Hash**\n [abcdabcd](https://kaiheila.cn)'),
                Kmarkdown('**Message**\n fix markdown (#97)')
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
