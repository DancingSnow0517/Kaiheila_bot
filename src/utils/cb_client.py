from typing import Awaitable, TYPE_CHECKING

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
        print(payload.author)
        with open('Temp/ChatBridge.txt', 'a', encoding='utf-8') as f:
            if payload.author == '':
                f.writelines(f'[{sender}] {payload.message}\n')
            else:
                f.writelines(f'[{sender}]<{payload.author}> {payload.message}\n')
