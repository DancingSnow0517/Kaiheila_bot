from khl import Bot, Message


def get_token() -> str:
    with open('TOKEN', 'r') as f:
        return f.read()


if __name__ == '__main__':
    khl_bot = Bot(token=get_token())

    @khl_bot.command(name='hello', prefixes=['!!', '！！'])
    async def world(msg: Message):
        await msg.ctx.channel.send('world')

    khl_bot.run()