import os.path

from khl import Bot

from ..config import Config


async def cb_pusher(bot: Bot, config: Config):
    if not os.path.exists('Temp/ChatBridge.txt'):
        return
    with open('Temp/ChatBridge.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    os.remove('Temp/ChatBridge.txt')

    for i in lines:
        msg = i.replace('\n', '')

        channel = await bot.client.fetch_public_channel(config.khl_channel_mc_chat)
        await channel.send(msg)
