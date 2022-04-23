import asyncio
from typing import TYPE_CHECKING

from .libs.chatbridge.core.client import ChatBridgeClient
from .libs.chatbridge.core.network.protocol import ChatPayload

if TYPE_CHECKING:
    from ..bot import KaiheilaBot


class KaiheilaClient(ChatBridgeClient):
    def __init__(self, bot: 'KaiheilaBot'):
        config = bot.config
        super().__init__(config.aes_key, config.client_info, server_address=config.server_address)
        self.config = config
        self.bot = bot
        self.loop = asyncio.get_event_loop()

    def on_chat(self, sender: str, payload: ChatPayload):
        self.loop.run_until_complete(self.send_msg(sender, payload))

    async def send_msg(self, sender: str, payload: ChatPayload):
        channel = await self.bot.client.fetch_public_channel(self.config.khl_channel_mc_chat)
        await channel.send(f'[{sender}] {payload.message}' if payload.author == '' else f'[{sender}]<{payload.author}> {payload.message}')
