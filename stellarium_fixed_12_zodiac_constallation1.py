import ephem
import math

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

# 定義星座對應的座標範圍
constellations_ranges = [
    (30, 60),
    (60, 90),
    (90, 118.75),
    (118.75, 128.75),
    (128.75, 166.25),
    (166.25, 188.75),
    (188.75, 215),
    (215, 240),
    (240, 270),
    (270, 300),
    (300, 326.25),
    (326.25, 350),
    (0, 30)
]

# 定義星座對應的座標點
constellations_coords = [
    (0, 0),
    (60, 0),
    (60, 60),
    (30, 60),
    (0, 60),
    (0, 30),
    (210, 0),
    (240, 0),
    (240, -10),
    (270, -10),
    (270, -30),
    (300, -30),
    (330, -30)
]

# 獲取太陽的視位置
sun = ephem.Sun(obs)
sun.compute()
sun_pos = math.degrees(sun.ra), math.degrees(sun.dec)

# 找到太陽所處的星座
constellation_idx = None
for idx, constellation_range in enumerate(constellations_ranges):
    if constellation_range[0] <= sun_pos[0] < constellation_range[1]:
        constellation_idx = idx
        break

# 打印結果
if constellation_idx is not None:
    print('The Sun is currently in the constellation:', constellations[constellation_idx])
    print('The coordinates of the constellation on the celestial sphere are:', constellations_coords[constellation_idx])
else:
    print('Cannot determine the current constellation of the Sun.')
