from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
import astropy.units as u
from gschedule.observer import Observer
from gschedule.target import Target
import math


# 计算天顶角
def get_ZenithAngle(observer: Observer, target: Target, time: str):
    # 观测者经纬度
    observer_location = EarthLocation(lat = observer.dec*u.deg, lon = observer.ra*u.deg, height = observer.elevation*u.m)

    # 创建一个时间对象
    # '2022-05-01 12:00:00'
    observation_time = Time(time)

    # 创建一个天顶角计算对象
    altaz = AltAz(location = observer_location, obstime = observation_time)

    # 获取某个天空点的天顶角
    target_coordinates = SkyCoord(ra = target.ra*u.deg, dec = target.dec*u.deg)
    target_altaz = target_coordinates.transform_to(altaz)

    # 输出天顶角的值
    zenith_angle = target_altaz.alt.degree
    # print(f"天顶角：{zenith_angle}度")
    # type(zenith_angle) = float
    return zenith_angle

# 计算airmass
def am(zenith):
    airmass = 1/math.cos(math.radians(zenith))
    return airmass