from typing import List


class _Text:
    type: str

    def build(self) -> dict:
        return {'type': self.type}


class plain_text(_Text):
    """
    构造纯文本
    """
    content: str

    def __init__(self, content: str = '') -> None:
        """
        构造纯文本

        :param content: 文本内容
        """
        self.type = 'plain-text'
        self.content = content

    def build(self) -> dict:
        return {'type': self.type, 'content': self.content}


class kmarkdown(_Text):
    """
    构造kmarkdown文本
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


class paragraph(_Text):
    """
    构造多列文本
    """
    cols: int
    fields: List[_Text]

    def __init__(self, cols: int, fields: List[_Text]) -> None:
        """
        构造多列文本

        :param cols: 列数
        :param fields: 文本组件列表
        """
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
