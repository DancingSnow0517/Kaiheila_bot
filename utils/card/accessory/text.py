from typing import List

from utils.card.accessory.accessory import base_Accessory


class base_Text(base_Accessory):
    """
    文字类元素基类
    """

    def build(self) -> dict:
        return {'type': self.type}


class plain_text(base_Text):
    """
    构造纯文本元素
    """
    content: str
    emoji: bool

    def __init__(self, content: str = '', emoji=True) -> None:
        """
        构造纯文本

        :param content: 文本内容
        :param emoji: 默认为 true。如果为 true,会把 emoji 的 shortcut 转为 emoji
        """
        self.type = 'plain-text'
        self.content = content
        self.emoji = emoji

    def build(self) -> dict:
        return {'type': self.type, 'content': self.content}


class kmarkdown(base_Text):
    """
    构造kmarkdown文本元素
    """
    content: str

    def __init__(self, content: str = '') -> None:
        """
        构造kmarkdown文本

        :param content: kmarkdown文本
        """
        self.type = 'kmarkdown'
        self.content = content

    def build(self) -> dict:
        return {'type': self.type, 'content': self.content}


class paragraph(base_Text):
    """
    构造多列文本元素
    """
    cols: int
    fields: List[base_Text]

    def __init__(self, cols: int, fields: List[base_Text]) -> None:
        """
        构造多列文本

        :param cols: 列数 只能为 1-3
        :param fields: 文本组件列表
        """
        if not (1 <= cols <= 3):
            raise Exception('文本列数不为 1-3')
        if len(fields) != cols:
            raise Exception('文本列数与列表不符')
        for i in fields:
            if isinstance(i, paragraph):
                raise Exception('文本组件不能为paragraph')
        self.type = 'paragraph'
        self.cols = cols
        self.fields

    def build(self) -> dict:
        ret = {'type': self.type, 'cols': self.cols, 'fields': []}
        for i in self.fields:
            ret['fields'].append(i.build())
        return ret
