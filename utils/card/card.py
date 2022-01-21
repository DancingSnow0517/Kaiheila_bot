from typing import Optional, List

from types import Theme, Size
from utils.card.modules import _module
from utils.color import Color


class Card:
    type: str = 'card'
    theme: str
    size: str
    color: Optional[Color]
    modules: List[_module]

    def __init__(self, theme: str = Theme.PRIMARY, size: str = Size.LG, color: Color = None) -> None:
        self.theme = theme
        self.size = size
        self.color = color

    def build(self) -> dict:
        ret = {'type': self.type, 'theme': self.theme, 'size': self.size}
        if self.color is not None:
            ret['color'] = self.color.__str__()

        return ret
