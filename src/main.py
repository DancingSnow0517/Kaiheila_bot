import logging

from khl import Bot, Message

from khl_card.accessory import *
from khl_card.modules import *
from khl_card.card import *

from utils.config import Config

if __name__ == '__main__':
    config = Config('config.json')
    config.read_from_json()

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
    khl_bot = Bot(token=config.token)
    logging.basicConfig(level='INFO', format='[%(asctime)s] [%(threadName)s/%(levelname)s]: %(message)s')


    @khl_bot.command(name='hello', prefixes=['!!', '！！'])
    async def world(msg: Message):
        await msg.reply('world')


    @khl_bot.command(name='test', prefixes=['!!', '！！'])
    async def test(msg: Message):
        await msg.reply([card.build()])


    khl_bot.run()
