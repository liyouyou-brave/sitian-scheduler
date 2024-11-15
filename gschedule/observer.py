
# 台站
class Observer:
    num: int
    name: str
    ra: float
    dec: float
    elevation: float

    # 初始化
    def __init__(self, num, name, ra, dec, elevation):
        self.num = num
        self.name = name
        self.ra = ra
        self.dec = dec
        self.elevation = elevation

