from datetime import datetime
import ephem  # 获取特定地点和日期时间的太阳高度角和方位角
from gschedule.observer import Observer

def calculate_sun_position(observer: Observer, date: str):
    obs = ephem.Observer()           # 观测者对象
    obs.lat, obs.lon, obs.elevation = observer.dec, observer.ra, observer.elevation     # 纬度 经度 海拔
    obs.date = ephem.Date(datetime.fromisoformat(date).strftime('%Y/%m/%d %H:%M:%S'))     # 观测时间
    # 定义要计算高度角的天体（如太阳、月亮等）
    sun = ephem.Sun(obs)  # 计算太阳的高度角
    # sun = ephem.Sun()
    # sun.compute(obs)
    return sun.alt   #, sun.az  # 返回太阳高度角和方位角


# latitude = 35.1
# longitude = 109.2
# date = '2021/12/22 9:00:00'  # 某一天的正午时间
# sun_altitude, sun_azimuth = calculate_sun_position(latitude, longitude, date)
# print(f"Sun altitude: {sun_altitude}, Sun azimuth: {sun_azimuth}")
# if sun_altitude < ephem.degrees('-18'):
#     print("Yes")
# else:
#     print("No")
