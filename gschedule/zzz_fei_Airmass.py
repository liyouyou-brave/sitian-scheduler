import math
from datetime import datetime

def calculate_airmass(latitude, longitude, right_ascension, declination, observer_altitude, observation_time):
    # 计算当地恒星时间（LST）
    utc_offset = longitude / 15  # 每15度一个小时
    lst = observation_time.hour + observation_time.minute / 60 + utc_offset

    # 计算时角H
    H = lst * 15 - right_ascension  # 将LST转换为度
    H = math.radians(H)

    # 将纬度和赤纬转换为弧度
    phi = math.radians(latitude)
    delta = math.radians(declination)

    # 计算高度角Z
    sin_Z = math.sin(phi) * math.sin(delta) + math.cos(phi) * math.cos(delta) * math.cos(H)
    Z = math.asin(sin_Z)

    # 计算气团
    airmass = 1 / math.cos(Z) if Z < math.pi / 2 else float('inf')  # Z必须小于90度

    # 考虑海拔高度对气团的影响
    pressure = 1013.25 * math.exp(-observer_altitude / 8434.5)  # 简化的气压计算（hPa）
    airmass *= pressure / 1013.25  # 标准气压下的气团

    return airmass


latitude = 40.0  # 观测者的纬度
longitude = -75.0  # 观测者的经度
right_ascension = 10.684  # 天体的赤经（单位：度）
declination = 41.269  # 天体的赤纬（单位：度）
observer_altitude = 1000  # 海拔高度（单位：米）
observation_time = datetime.utcnow()  # 当前UTC时间

airmass = calculate_airmass(latitude, longitude, right_ascension, declination, observer_altitude, observation_time)
print(f"Airmass: {airmass}")
