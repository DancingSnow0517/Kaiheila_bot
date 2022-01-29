from typing import Awaitable, TYPE_CHECKING
import asyncio

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

    def on_chat(self, sender: str, payload: ChatPayload):
        channel = sync(self.bot.client.fetch_public_channel(self.config.khl_channel_mc_chat))
        asyncio.run(channel.send("[{}]<{}> {}".format(sender, payload.author, payload.message)))
