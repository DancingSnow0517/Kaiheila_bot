from utils.card.accessory.accessory import base_Accessory
from utils.card.types import Theme


class base_Non_text(base_Accessory):
    """
    非文字类元素基类
    """
    def build(self) -> dict:
        return {'type': self.type}


class image(base_Non_text):
    """
    显示图片元素
    """
    src: str
    alt: str
    size: str
    circle: bool

    def __init__(self, src: str, size: str = 'lg', alt: str = '', circle: bool = False) -> None:
        """
        显示图片元素

        :param src: 图片地址
        :param size: 图片大小样式 只能为 sm 或 lg
        :param alt: 不知道干嘛用的
        :param circle: 显示圆形图片，在文本+图片时有效
        """
        self.type = 'image'
        self.src = src
        self.alt = alt
        self.size = size
        self.circle = circle

    def build(self) -> dict:
        return {'type': self.type, 'src': self.src, 'alt': self.alt, 'size': self.size, 'circle': self.circle}


class button(base_Non_text):
    theme: str
    value: str
    click: str
    text: str

    def __init__(self, text: str, theme: str = Theme.PRIMARY, value: str = '', click: str = '') -> None:
        self.type = 'button'
        self.text = text
        self.theme = theme
        self.value = value
        self.click = click

    def build(self) -> dict:
        return {'type': self.type, 'theme': self.theme, 'value': self.theme, 'click': self.click, 'text': self.text}

