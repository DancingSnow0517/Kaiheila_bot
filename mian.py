from khl import Bot, Message
import logging


def get_token() -> str:
    with open('TOKEN', 'r') as f:
        return f.read()


if __name__ == '__main__':
    khl_bot = Bot(token=get_token())
    logging.basicConfig(level='INFO')

    @khl_bot.command(name='hello', prefixes=['!!', '！！'])
    async def world(msg: Message):
        await msg.reply('world')

    khl_bot.run()