import time
from typing import List

from utils.card.accessory.accessory import base_Accessory
from utils.card.accessory.non_text import base_Non_text, image, button
from utils.card.accessory.text import plain_text, base_Text


class _module:
    """
    模块基类
    """
    type: str

    def build(self) -> dict:
        """
        构建模块

        :return: 构造后模块
        """
        return {'type': self.type}


class header(_module):
    """
    构建标题模块

    标题模块只能支持展示标准文本（text），突出标题样式。
    """
    text: plain_text

    def __init__(self, text: str = '') -> None:
        """
        构建标题模块

        标题模块只能支持展示标准文本（text），突出标题样式。

        :param text: 标题内容
        """
        self.type = 'header'
        self.text = plain_text(content=text)

    def build(self) -> dict:
        return {"type": self.type, "text": self.text.build()}


class section(_module):
    """
    构建内容模块

     结构化的内容，显示文本+其它元素。
    """
    mode: str
    text: base_Text
    accessory: base_Non_text

    def __init__(self, mode: str, text: base_Text, accessory: base_Non_text) -> None:
        """
        构建内容模块

        结构化的内容，显示文本+其它元素。

        :param mode: accessory在左侧还是在右侧 只能为 left|right
        :param text: 文本元素
        :param accessory: 非文本元素
        """
        self.type = 'section'
        self.mode = mode
        self.text = text
        self.accessory = accessory

    def build(self) -> dict:
        return {'type': self.type, 'mode': self.mode, 'text': self.text.build(), 'accessory': self.accessory.build()}


class image_group(_module):
    """
    构建图片组模块

    1 到多张图片的组合
    """
    elements: List[image]

    def __init__(self, elements: List[image]) -> None:
        """
        构建图片组模块

        1 到多张图片的组合

        :param elements: 图片元素，其它元素无效
        """
        self.type = 'image-group'
        if len(elements) > 9:
            raise Exception('图片元素最多为9个')
        self.elements = elements

    def build(self) -> dict:
        ret = {'type': self.type, 'elements': []}
        for i in self.elements:
            ret['elements'].append(i.build())
        return ret


class container(_module):
    """
    构建容器模块
    """
    elements: List[image]

    def __init__(self, elements: List[image]) -> None:
        """
        构建容器模块

        1 到多张图片的组合，与图片组模块不同，图片并不会裁切为正方形。多张图片会纵向排列。

        :param elements: 图片元素，其它元素无效
        """
        self.type = 'image-group'
        if len(elements) > 9:
            raise Exception('图片元素最多为9个')
        self.elements = elements

    def build(self) -> dict:
        ret = {'type': self.type, 'elements': []}
        for i in self.elements:
            ret['elements'].append(i.build())
        return ret


class action_group(_module):
    """
    构建交互模块

    交互模块中包含交互控件元素，目前支持的交互控件为按钮（button）
    """
    elements: List[button]

    def __init__(self, elements: List[button]) -> None:
        """
        构建交互模块

        交互模块中包含交互控件元素，目前支持的交互控件为按钮（button）

        :param elements: 按钮元素，其他无效
        """
        self.type = 'action-group'
        if len(elements) > 4:
            raise Exception('按钮元素最多为4个')
        self.elements = elements

    def build(self) -> dict:
        ret = {'type': self.type, 'elements': []}
        for i in self.elements:
            ret['elements'].append(i.build())
        return ret


class context(_module):
    """
    构建备注模块

    展示图文混合的内容。
    """
    elements: List[base_Accessory]

    def __init__(self, elements: List[base_Accessory]) -> None:
        """
        构建备注模块

        展示图文混合的内容

        :param elements: 文本元素以及图片元素
        """
        self.type = 'context'
        if len(elements) > 10:
            raise Exception('元素最多为10个')
        self.elements = elements

    def build(self) -> dict:
        ret = {'type': self.type, 'elements': []}
        for i in self.elements:
            ret['elements'].append(i.build())
        return ret


class divider(_module):
    """
    构建分割线模块

    展示分割线。
    """

    def __init__(self) -> None:
        """
        构建分割线模块

        展示分割线。
        """
        self.type = 'divider'

    def build(self) -> dict:
        return {'type': self.type}


class countdown(_module):
    """
    构建倒计时模块

    展示倒计时。
    """
    endTime: int
    startTime: int
    mode: str

    def __init__(self, endTime: int, mode: str, startTime: int = time.time() * 1000) -> None:
        """
        构建倒计时模块

        展示倒计时

        :param mode: 倒计时样式, 按天显示，按小时显示或者按秒显示
        :param endTime: 到期的毫秒时间戳
        :param startTime: 起始的毫秒时间戳，仅当mode为second才有这个字段，默认为当前时间
        """
        self.type = 'countdown'
        if mode != 'day' and mode != 'hour' and mode != 'second':
            raise Exception('mode必须为 day|hour|second')
        if endTime > startTime:
            raise Exception('结束时间要大于开始时间')
        self.endTime = endTime
        self.startTime = startTime

    def build(self) -> dict:
        return {'type': self.type, 'mode': self.mode, 'endTime': self.endTime, 'startTime': self.startTime}


class invite(_module):
    """
    构建邀请模块

    提供服务器邀请/语音频道邀请
    """
    code: str

    def __init__(self, code: str) -> None:
        """
        构建邀请模块

        提供服务器邀请/语音频道邀请

        :param code: 邀请链接或者邀请码
        """
        self.type = 'invite'
        self.code = code

    def build(self) -> dict:
        return {'type': self.type, 'code': self.code}


class _file_module(_module):
    """
    文件模块基类
    """
    src: str
    title: str

    def __init__(self, src: str, title: str) -> None:
        self.src = src
        self.title = title

    def build(self) -> dict:
        return {'type': self.type, 'src': self.src, 'title': self.title}


class file(_file_module):
    """
    构建文件模块

    展示文件
    """

    def __init__(self, src: str, title: str) -> None:
        """
        :param src: 文件地址
        :param title: 标题
        """
        super().__init__(src, title)


class video(_file_module):
    """
    构建视频模块

    展示视频
    """

    def __init__(self, src: str, title: str) -> None:
        """
        构建视频模块

        展示视频

        :param src: 视频地址
        :param title: 标题
        """
        super().__init__(src, title)


class audio(_file_module):
    """
    构建音频模块

    展示音频
    """
    cover: str

    def __init__(self, src: str, title: str, cover: str) -> None:
        """
        构建音频模块

        展示音频

        :param src: 音频地址
        :param title: 标题
        :param cover: 封面地址
        """
        super().__init__(src, title)
        self.cover = cover

    def build(self) -> dict:
        ret = super().build()
        ret['cover'] = self.cover
        return ret
