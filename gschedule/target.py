
# 天区
class Target:
    num: int
    ra: float
    dec: float
    last_time: int
    total_timenum: int
    filter: int            # 滤光片
    user_prior: int
    am: list

    # 初始化
    def __init__(self, num, ra, dec, last_time, total_timenum, filter, user_prior):
        self.num = num
        self.ra = ra
        self.dec = dec
        self.last_time = last_time
        self.total_timenum = total_timenum
        self.filter = filter
        self.user_prior = user_prior
        self.am = []

    # # 字符串表示形式
    # def __str__(self):
    #     return f"Target(num={self.num}, minute={self.minute})"

    # my_target = Target(1, 10)
    # print(my_target)

