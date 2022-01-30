import base64
import os.path

from khl import Bot
from khl_card.card import Card
from khl_card.modules import *
from khl_card.accessory import *


class Dynamic:
    msg_card: Card

    def __init__(self, dynamic):
        # self.origin = json.loads(self.card['origin'])
        self.dynamic = dynamic
        # self.card = json.loads(dynamic['card'])
        # self.dynamic['card'] = self.card
        self.type = dynamic['desc']['type']
        self.id = dynamic['desc']['dynamic_id']
        self.url = "https://t.bilibili.com/" + str(self.id)
        self.time = dynamic['desc']['timestamp']
        # self.origin_id = dynamic['desc']['orig_dy_id']
        self.uid = dynamic['desc']['user_profile']['info']['uid']
        self.name = dynamic['desc']['user_profile']['info'].get('uname')
        # self.name = dynamic['desc']['user_profile']['info'].get('uname', Config.get_name(self.uid))

    async def format(self, img, bot: Bot):
        type_msg = {
            0: "发布了新动态",
            1: "转发了一条动态",
            8: "发布了新投稿",
            16: "发布了短视频",
            64: "发布了新专栏",
            256: "发布了新音频"
        }
        # self.message = (f"{self.name} " +
        #                f"{type_msg.get(self.type, type_msg[0])}：\n" +
        #                 f"{self.url}\n" +
        #                 MessageSegment.image(f"base64://{img}")
        #                 )
        if not os.path.exists('Temp'):
            os.makedirs('Temp')
        with open(f'Temp/{self.uid}.png', 'wb') as f:
            img_data = base64.b64decode(img)
            f.write(img_data)

        image_url = await bot.upload_asset(f'Temp/{self.uid}.png')

        self.msg_card = Card([
            Header(f'{self.name} {type_msg.get(self.type, type_msg[0])}'),
            Section(Kmarkdown(f'[网页链接]({self.url})')),
            Container([Image(image_url)])
        ])
