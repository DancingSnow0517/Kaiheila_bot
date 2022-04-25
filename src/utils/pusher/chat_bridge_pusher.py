from ..config import Config

from khl import MessageTypes


async def cb_pusher(bot, config: Config):
    for i in bot.cb_temp:
        bot.cb_temp.remove(i)
        channel = await bot.client.fetch_public_channel(config.khl_channel_mc_chat)
        await channel.send(i, type=MessageTypes.KMD)
