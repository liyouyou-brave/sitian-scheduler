from gschedule.observer import Observer
from gschedule.target import Target

#SBlock
class Sblock:
    total_exp_time: int
    target: Target
    site: Observer
    start_time: str

    def __init__(self, total_exp_time, target, site, start_time):
        self.total_exp_time = total_exp_time
        self.target = target
        self.site = site
        self.start_time = start_time
