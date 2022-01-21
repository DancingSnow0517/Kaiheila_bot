class Color:
    R: int
    G: int
    B: int

    def __init__(self, r: int, g: int, b: int) -> None:
        if r > 255 or g > 255 or b > 255:
            raise Exception('RGB数字必须为0-255')
        if r < 0 or g < 0 or b < 0:
            raise Exception('RGB数字必须为0-255')
        self.R = r
        self.G = g
        self.B = b

    def __str__(self) -> str:
        return f'#{hex(self.R)}{hex(self.G)}{hex(self.B)}'
