import ephem
import math
from ephem import constellation


# 設置日期和地點
date = '2023/3/23 12:00:00'
lon = '121.5654'  # 經度
lat = '25.0330'  # 緯度
alt = 0  # 高度，以度為單位

# 初始化天體對象
obs = ephem.Observer()
obs.date = date
obs.lon = lon
obs.lat = lat
obs.elevation = alt

# 定義星座列表
constellations = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpius', 'Ophiuchus', 'Sagittarius', 'Capricornus', 'Aquarius', 'Pisces']

# 載入星座邊界數據庫文件
ephem.constellation.load('skycultures/modern_sternenkarten/constellationship.fab')

# 加載星座邊界數據庫
constellation_boundaries = ephem.readdb('Stellarium:constellationship.fab')

# 定義函數，用於獲取黃道經度
def get_ecliptic_longitude(ra, dec):
    eq = ephem.Equatorial(ra, dec)
    ecl = ephem.Ecliptic(eq)
    return math.degrees(ecl.lon)

# 定義函數，用於獲取黃道緯度
def get_ecliptic_latitude(ra, dec):
    eq = ephem.Equatorial(ra, dec)
    ecl = ephem.Ecliptic(eq)
    return math.degrees(ecl.lat)

# 獲取太陽的視位置
sun = ephem.Sun(obs)
sun.compute()
sun_ra, sun_dec = sun.ra, sun.dec

# 找到太陽所處的星座
constellation_idx = None
for idx, constellation in enumerate(constellations):
    ra, dec = constellation_boundaries.get(constellation)
    ecl_long = get_ecliptic_longitude(ra, dec)
    ecl_lat = get_ecliptic_latitude(ra, dec)
    if ecl_long < 0:
        ecl_long += 360
    if ecl_long > 180:
        ecl_long -= 360
    if ecl_long <= get_ecliptic_longitude(sun_ra, sun_dec) < ecl_long + 30 and ecl_lat >= 0:
        constellation_idx = idx
        break

# 打印結果
if constellation_idx is not None:
    print('The Sun is currently in the constellation:', constellations[constellation_idx])
    ra, dec = constellation_boundaries.get(constellations[constellation_idx])
    print('The coordinates of the constellation on the ecliptic are:', get_ecliptic_longitude(ra, dec), get_ecliptic_latitude(ra, dec))
else:
    print('Cannot determine the current constellation of the Sun.')