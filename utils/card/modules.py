from utils.text import plain_text


class _module:
    type: str

    def build(self) -> dict:
        return {'type': self.type}


class header(_module):
    """
    构建标题模块
    """
    text: plain_text

    def __init__(self, text: str = '') -> None:
        """
        构建标题模块

        :param text: 标题内容
        """
        self.type = 'header'
        self.text = plain_text(content=text)

    def build(self) -> dict:
        return {"type": self.type, "text": self.text.build()}
