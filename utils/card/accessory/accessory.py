class base_Accessory:
    """
    元素基类
    """
    type: str

    def build(self) -> dict:
        """
        :return: 构造后元素
        """
        return {'type': self.type}
