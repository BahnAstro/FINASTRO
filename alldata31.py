 #======================== Part 1: 数据生成 ========================
#這版本的錯誤在於八字的年、月、日柱“

import swisseph as swe
import pandas as pd
from datetime import datetime, timezone, timedelta
import cnlunar
from lunar_python import LunarYear
from collections import defaultdict
from tqdm import tqdm  # 用于显示进度条

# 读取输入 CSV 文件
readdata1 = pd.read_csv(
    "/Users/jacky/Desktop/DESKTOP/HSI/HSI_HL_2006to2023_updated.csv",
    header=None,
    skiprows=1,
    names=['datetime', 'value', 'type'],
    encoding='ISO-8859-1'
)

# 将 'datetime' 列转换为 pandas datetime 对象，并设置为 UTC 时区感知
readdata1['datetime'] = pd.to_datetime(
    readdata1['datetime'],
    format='%Y-%m-%d %H:%M:%S',
    utc=True
)

# 设置地理位置纬度和经度
latitude = 22.283875
longitude = 114.158229

# 定義六十甲子納音五行映射，並將元素轉換為英文
nayin_elements_chinese = {
    '甲子': 'metal', '乙丑': 'metal',
    '丙寅': 'fire', '丁卯': 'fire',
    '戊辰': 'wood', '己巳': 'wood',
    '庚午': 'earth', '辛未': 'earth',
    '壬申': 'metal', '癸酉': 'metal',
    '甲戌': 'fire', '乙亥': 'fire',
    '丙子': 'water', '丁丑': 'water',
    '戊寅': 'earth', '己卯': 'earth',
    '庚辰': 'metal', '辛巳': 'metal',
    '壬午': 'wood', '癸未': 'wood',
    '甲申': 'water', '乙酉': 'water',
    '丙戌': 'earth', '丁亥': 'earth',
    '戊子': 'fire', '己丑': 'fire',
    '庚寅': 'wood', '辛卯': 'wood',
    '壬辰': 'water', '癸巳': 'water',
    '甲午': 'metal', '乙未': 'metal',
    '丙申': 'fire', '丁酉': 'fire',
    '戊戌': 'wood', '己亥': 'wood',
    '庚子': 'earth', '辛丑': 'earth',
    '壬寅': 'metal', '癸卯': 'metal',
    '甲辰': 'fire', '乙巳': 'fire',
    '丙午': 'water', '丁未': 'water',
    '戊申': 'earth', '己酉': 'earth',
    '庚戌': 'metal', '辛亥': 'metal',
    '壬子': 'wood', '癸丑': 'wood',
    '甲寅': 'water', '乙卯': 'water',
    '丙辰': 'earth', '丁巳': 'earth',
    '戊午': 'fire', '己未': 'fire',
    '庚申': 'wood', '辛酉': 'wood',
    '壬戌': 'water', '癸亥': 'water'
}


# 定义洞微大限（五行年限度数），以年份为键，度数范围为值
year_degrees = {
    "year_2005": [230.216666667, 228.216666667],
    "year_2006": [228.216666667, 226.216666667],
    "year_2007": [226.216666667, 224.216666667],
    "year_2008": [224.216666667, 222.216666667],
    "year_2009": [222.216666667, 220.216666667],
    "year_2010": [220.216666667, 218.216666667],
    "year_2011": [218.216666667, 216.216666667],
    "year_2012": [216.216666667, 214.216666667],
    "year_2013": [214.216666667, 212.216666667],
    "year_2014": [212.216666667, 210.216666667],
    "year_2015": [210.216666667, 206.65],
    "year_2016": [206.65, 202.883333333],
    "year_2017": [202.883333333, 199.15],
    "year_2018": [199.15, 195.4],
    "year_2019": [195.4, 191.65],
    "year_2020": [191.65, 187.883333333],
    "year_2021": [187.883333333, 184.15],
    "year_2022": [184.15, 180.4],
    "year_2023": [180.4, 176.166666667]
}

# 定义十二長生映射
changsheng_mapping = {
    # 長生
    ('甲', '亥'): '長生',
    ('丙', '寅'): '長生',
    ('戊', '寅'): '長生',
    ('庚', '巳'): '長生',
    ('壬', '申'): '長生',
    ('乙', '午'): '長生',
    ('丁', '酉'): '長生',
    ('己', '酉'): '長生',
    ('辛', '子'): '長生',
    ('癸', '卯'): '長生',

    # 沐浴
    ('甲', '子'): '沐浴',
    ('丙', '卯'): '沐浴',
    ('戊', '卯'): '沐浴',
    ('庚', '午'): '沐浴',
    ('壬', '酉'): '沐浴',
    ('乙', '巳'): '沐浴',
    ('丁', '申'): '沐浴',
    ('己', '申'): '沐浴',
    ('辛', '亥'): '沐浴',
    ('癸', '寅'): '沐浴',

    # 冠帶
    ('甲', '丑'): '冠帶',
    ('丙', '辰'): '冠帶',
    ('戊', '辰'): '冠帶',
    ('庚', '未'): '冠帶',
    ('壬', '戌'): '冠帶',
    ('乙', '辰'): '冠帶',
    ('丁', '未'): '冠帶',
    ('己', '未'): '冠帶',
    ('辛', '戌'): '冠帶',
    ('癸', '丑'): '冠帶',

    # 臨官
    ('甲', '寅'): '臨官',
    ('丙', '巳'): '臨官',
    ('戊', '巳'): '臨官',
    ('庚', '申'): '臨官',
    ('壬', '亥'): '臨官',
    ('乙', '卯'): '臨官',
    ('丁', '午'): '臨官',
    ('己', '午'): '臨官',
    ('辛', '酉'): '臨官',
    ('癸', '子'): '臨官',

    # 帝旺
    ('甲', '卯'): '帝旺',
    ('丙', '午'): '帝旺',
    ('戊', '午'): '帝旺',
    ('庚', '酉'): '帝旺',
    ('壬', '子'): '帝旺',
    ('乙', '寅'): '帝旺',
    ('丁', '巳'): '帝旺',
    ('己', '巳'): '帝旺',
    ('辛', '申'): '帝旺',
    ('癸', '亥'): '帝旺',

    # 衰
    ('甲', '辰'): '衰',
    ('丙', '未'): '衰',
    ('戊', '未'): '衰',
    ('庚', '戌'): '衰',
    ('壬', '丑'): '衰',
    ('乙', '丑'): '衰',
    ('丁', '辰'): '衰',
    ('己', '辰'): '衰',
    ('辛', '未'): '衰',
    ('癸', '戌'): '衰',

    # 病
    ('甲', '巳'): '病',
    ('丙', '申'): '病',
    ('戊', '申'): '病',
    ('庚', '亥'): '病',
    ('壬', '寅'): '病',
    ('乙', '子'): '病',
    ('丁', '卯'): '病',
    ('己', '卯'): '病',
    ('辛', '午'): '病',
    ('癸', '酉'): '病',

    # 死
    ('甲', '午'): '死',
    ('丙', '酉'): '死',
    ('戊', '酉'): '死',
    ('庚', '子'): '死',
    ('壬', '卯'): '死',
    ('乙', '亥'): '死',
    ('丁', '寅'): '死',
    ('己', '寅'): '死',
    ('辛', '巳'): '死',
    ('癸', '申'): '死',

    # 墓
    ('甲', '未'): '墓',
    ('丙', '戌'): '墓',
    ('戊', '戌'): '墓',
    ('庚', '丑'): '墓',
    ('壬', '辰'): '墓',
    ('乙', '戌'): '墓',
    ('丁', '丑'): '墓',
    ('己', '丑'): '墓',
    ('辛', '辰'): '墓',
    ('癸', '未'): '墓',

    # 絕
    ('甲', '申'): '絕',
    ('丙', '亥'): '絕',
    ('戊', '亥'): '絕',
    ('庚', '寅'): '絕',
    ('壬', '巳'): '絕',
    ('乙', '酉'): '絕',
    ('丁', '子'): '絕',
    ('己', '子'): '絕',
    ('辛', '卯'): '絕',
    ('癸', '午'): '絕',

    # 胎
    ('甲', '酉'): '胎',
    ('丙', '子'): '胎',
    ('戊', '子'): '胎',
    ('庚', '卯'): '胎',
    ('壬', '午'): '胎',
    ('乙', '申'): '胎',
    ('丁', '亥'): '胎',
    ('己', '亥'): '胎',
    ('辛', '寅'): '胎',
    ('癸', '巳'): '胎',

    # 養
    ('甲', '戌'): '養',
    ('丙', '丑'): '養',
    ('戊', '丑'): '養',
    ('庚', '辰'): '養',
    ('壬', '未'): '養',
    ('乙', '未'): '養',
    ('丁', '戌'): '養',
    ('己', '戌'): '養',
    ('辛', '丑'): '養',
    ('癸', '辰'): '養',
}

# 定義天干五行陰陽映射（英文）
heavenly_stems_mapping = {
    '甲': {'element': 'wood', 'yin_yang': 'yang'},
    '乙': {'element': 'wood', 'yin_yang': 'yin'},
    '丙': {'element': 'fire', 'yin_yang': 'yang'},
    '丁': {'element': 'fire', 'yin_yang': 'yin'},
    '戊': {'element': 'earth', 'yin_yang': 'yang'},
    '己': {'element': 'earth', 'yin_yang': 'yin'},
    '庚': {'element': 'metal', 'yin_yang': 'yang'},
    '辛': {'element': 'metal', 'yin_yang': 'yin'},
    '壬': {'element': 'water', 'yin_yang': 'yang'},
    '癸': {'element': 'water', 'yin_yang': 'yin'}
}

# 定義地支五行陰陽映射（中文，繁體）
earthly_branches_mapping = {
    '子': {'element': 'water', 'yin_yang': 'yang'},
    '丑': {'element': 'earth', 'yin_yang': 'yin'},
    '寅': {'element': 'metal', 'yin_yang': 'yang'},
    '卯': {'element': 'metal', 'yin_yang': 'yin'},
    '辰': {'element': 'earth', 'yin_yang': 'yang'},
    '巳': {'element': 'fire', 'yin_yang': 'yin'},
    '午': {'element': 'fire', 'yin_yang': 'yang'},
    '未': {'element': 'earth', 'yin_yang': 'yin'},
    '申': {'element': 'metal', 'yin_yang': 'yang'},
    '酉': {'element': 'metal', 'yin_yang': 'yin'},
    '戌': {'element': 'earth', 'yin_yang': 'yang'},
    '亥': {'element': 'water', 'yin_yang': 'yin'}
}

# 定义分钟柱映射（0-59）
minute_pillar_mapping = {
    0: ('癸', '亥'),
    1: ('甲', '子'),
    2: ('乙', '丑'),
    3: ('丙', '寅'),
    4: ('丁', '卯'),
    5: ('戊', '辰'),
    6: ('己', '巳'),
    7: ('庚', '午'),
    8: ('辛', '未'),
    9: ('壬', '申'),
    10: ('癸', '酉'),
    11: ('甲', '戌'),
    12: ('乙', '亥'),
    13: ('丙', '子'),
    14: ('丁', '丑'),
    15: ('戊', '寅'),
    16: ('己', '卯'),
    17: ('庚', '辰'),
    18: ('辛', '巳'),
    19: ('壬', '午'),
    20: ('癸', '未'),
    21: ('甲', '申'),
    22: ('乙', '酉'),
    23: ('丙', '戌'),
    24: ('丁', '亥'),
    25: ('戊', '子'),
    26: ('己', '丑'),
    27: ('庚', '寅'),
    28: ('辛', '卯'),
    29: ('壬', '辰'),
    30: ('癸', '巳'),
    31: ('甲', '午'),
    32: ('乙', '未'),
    33: ('丙', '申'),
    34: ('丁', '酉'),
    35: ('戊', '戌'),
    36: ('己', '亥'),
    37: ('庚', '子'),
    38: ('辛', '丑'),
    39: ('壬', '寅'),
    40: ('癸', '卯'),
    41: ('甲', '辰'),
    42: ('乙', '巳'),
    43: ('丙', '午'),
    44: ('丁', '未'),
    45: ('戊', '申'),
    46: ('己', '酉'),
    47: ('庚', '戌'),
    48: ('辛', '亥'),
    49: ('壬', '子'),
    50: ('癸', '丑'),
    51: ('甲', '寅'),
    52: ('乙', '卯'),
    53: ('丙', '辰'),
    54: ('丁', '巳'),
    55: ('戊', '午'),
    56: ('己', '未'),
    57: ('庚', '申'),
    58: ('辛', '酉'),
    59: ('壬', '戌'),
}

def calculate_year_degree(year_pillar, lunar_year, lunar_month, lunar_day, is_leap_month):
    """
    计算洞微大限的度数和对应的五行，根据年份柱。
    """
    # 确保 year_pillar 格式正确
    year_pillar = str(year_pillar).strip()

    key = f"year_{lunar_year}"
    if key not in year_degrees:
        return 330, 'unknown'  # 默认值和未知五行

    start_degree, end_degree = year_degrees[key]

    # 使用 lunar_python 库获取农历年份信息
    lunarYear = LunarYear.fromYear(lunar_year)
    day_count = lunarYear.getDayCount()
    # 计算当前日期是当年的第几天
    day_index = sum(
        lunarYear.getMonth(m).getDayCount()
        for m in range(1, lunar_month)
    ) + lunar_day

    if is_leap_month:
        day_index += lunarYear.getMonth(lunar_month).getDayCount()

    # 线性插值计算年限度数python
    year_degree = start_degree + (end_degree - start_degree) * (day_index - 1) / (day_count - 1)

    # year_degree_wuxing 就是纳音五行
    year_degree_wuxing = nayin_elements_chinese.get(year_pillar, 'unknown')

    # 调试输出，确保映射正确
    if year_degree_wuxing == 'unknown':
        print(f"警告：未找到年柱 '{year_pillar}' 的纳音五行映射。")

    return year_degree, year_degree_wuxing

def calc_asc_mc(jd, latitude, longitude):
    """
    计算上升点（asc）和中天点（mc）。
    """
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    ascendant = ascmc[0]
    midheaven = ascmc[1]
    descendant = cusps[6]
    imum_coeli = cusps[3]
    equ_ascendant = ascmc[4]
    return ascendant, midheaven, descendant, imum_coeli, equ_ascendant

def calculate_fortune(ascendant, sun_long, moon_long, jd, latitude, longitude):
    """
    计算福德点（part_of_fortune）。
    """
    geopos = (longitude, latitude, 0)
    # 计算日出和日落时间
    res_sunrise = swe.rise_trans(jd, swe.SUN, 0, swe.CALC_RISE | swe.BIT_DISC_CENTER, *geopos)
    res_sunset = swe.rise_trans(jd, swe.SUN, 0, swe.CALC_SET | swe.BIT_DISC_CENTER, *geopos)
    jd_sunrise = res_sunrise[1][0]
    jd_sunset = res_sunset[1][0]
    # 检查当前时间是否在日出和日落之间
    is_daytime = jd_sunrise <= jd < jd_sunset
    # 计算福德点
    if is_daytime:
        fortune_long = ascendant + moon_long - sun_long
    else:
        fortune_long = ascendant + sun_long - moon_long
    return fortune_long % 360


def solar_terms(ecl_lon):
    """
    根据黄经计算节气。
    24节气，每个节气对应的黄经为15度：
    立春 (315°), 雨水 (330°), 惊蛰 (345°), 春分 (0°), 清明 (15°), 谷雨 (30°),
    立夏 (45°), 小满 (60°), 芒种 (75°), 夏至 (90°), 小暑 (105°), 大暑 (120°),
    立秋 (135°), 处暑 (150°), 白露 (165°), 秋分 (180°), 寒露 (195°), 霜降 (210°),
    立冬 (225°), 小雪 (240°), 大雪 (255°), 冬至 (270°), 小寒 (285°), 大寒 (300°)
    """
    terms = [
        (315, '立春'), (330, '雨水'), (345, '驚蟄'), (0, '春分'),
        (15, '清明'), (30, '穀雨'), (45, '立夏'), (60, '小滿'),
        (75, '芒種'), (90, '夏至'), (105, '小暑'), (120, '大暑'),
        (135, '立秋'), (150, '處暑'), (165, '白露'), (180, '秋分'),
        (195, '寒露'), (210, '霜降'), (225, '立冬'), (240, '小雪'),
        (255, '大雪'), (270, '冬至'), (285, '小寒'), (300, '大寒')
    ]
    for i, (deg, name) in enumerate(terms):
        next_deg = terms[(i + 1) % len(terms)][0]
        if deg < next_deg:
            if deg <= ecl_lon < next_deg:
                return name
        else:  # 跨越0度
            if ecl_lon >= deg or ecl_lon < next_deg:
                return name
    return '未知'


def zodiac_sign(ecl_lon):
     """
     根据黄经计算西方占星的星座及其度数（英文）。
     """
     if ecl_lon is None or not isinstance(ecl_lon, (int, float)):
         return ('Unknown', 'unknown', 0)

     signs = {
         (0, 30): 'Aries_fire',
         (30, 60): 'Taurus_metal',
         (60, 90): 'Gemini_water',
         (90, 120): 'Cancer_moon',
         (120, 150): 'Leo_sun',
         (150, 180): 'Virgo_water',
         (180, 210): 'Libra_metal',
         (210, 240): 'Scorpio_fire',
         (240, 270): 'Sagittarius_wood',
         (270, 300): 'Capricorn_earth',
         (300, 330): 'Aquarius_earth',
         (330, 360): 'Pisces_wood'
     }
     for (start, end), sign in signs.items():
         if start <= ecl_lon < end:
             degree = ecl_lon - start
             sign_name, sign_element = sign.split("_")
             return sign_name, sign_element.lower(), degree
     return 'Unknown', 'unknown', 0


def mansion_position(ecl_lon):
     """
     根据黄经计算中国占星的28宿位置及其元素（英文）。
     """
     if ecl_lon is None or not isinstance(ecl_lon, (int, float)):
         return ('Unknown', 0, 'unknown')

     ecl_lon %= 360  # 确保 ecl_lon 在 0-360 度范围内
     positions = {
         (203.8374893, 214.4898543): '角宿_Horn',
         (214.4898543, 225.0215638): '亢宿_Neck',
         (225.0215638, 242.9360091): '氐宿_Root',
         (242.9360091, 249.7584245): '房宿_Room',
         (249.7584245, 256.1517382): '心宿_Heart',
         (256.1517382, 271.2575671): '尾宿_Tail',
         (271.2575671, 280.1774751): '箕宿_Winnowing_Basket',
         (280.1774751, 304.0435179): '斗宿_Dipper',
         (304.0435179, 311.7193257): '牛宿_Ox',
         (311.7193257, 323.3911983): '女宿_Girl',
         (323.3911983, 333.348599): '虛宿_Emptiness',
         (333.348599, 353.481734): '危宿_Rooftop',
         (353.481734, 9.152166707): '室宿_Encampment',
         (9.152166707, 22.37214699): '壁宿_Wail',
         (22.37214699, 33.96614257): '奎宿_Legs',
         (33.96614257, 46.93116249): '婁宿_Bond',
         (46.93116249, 59.40804317): '胃宿_Stomach',
         (59.40804317, 68.46117549): '昴宿_Hairy_Head',
         (68.46117549, 83.70296314): '畢宿_Net',
         (83.70296314, 84.67745824): '觜宿_Turtle_Beak',
         (84.67745824, 95.29802279): '參宿_Three_Stars',
         (95.29802279, 125.7245614): '井宿_Well',
         (125.7245614, 130.3004766): '鬼宿_Ghost',
         (130.3004766, 147.275341): '柳宿_Willow',
         (147.275341, 155.6873952): '星宿_Star',
         (155.6873952, 173.6855706): '張宿_Extended_Net',
         (173.6855706, 190.7217613): '翼宿_Wings',
         (190.7217613, 203.8374893): '軫宿_Chariot'
     }
     elements = {
         'wood': ['角宿_Horn', '斗宿_Dipper', '奎宿_Legs', '井宿_Well'],
         'metal': ['亢宿_Neck', '牛宿_Ox', '婁宿_Bond', '鬼宿_Ghost'],
         'earth': ['氐宿_Root', '女宿_Girl', '胃宿_Stomach', '柳宿_Willow'],
         'sun_element': ['房宿_Room', '虛宿_Emptiness', '昴宿_Hairy_Head', '星宿_Star'],
         'moon_element': ['心宿_Heart', '危宿_Rooftop', '畢宿_Net', '張宿_Extended_Net'],
         'fire': ['尾宿_Tail', '室宿_Encampment', '觜宿_Turtle_Beak', '翼宿_Wings'],
         'water': ['箕宿_Winnowing_Basket', '壁宿_Wail', '參宿_Three_Stars', '軫宿_Chariot']
     }
     for (start, end), position in positions.items():
         if position == '室宿_Encampment':
             if (start <= ecl_lon < 360) or (0 <= ecl_lon < end):
                 degree = ecl_lon - start if ecl_lon >= start else ecl_lon
                 for element, mansions in elements.items():
                     if position.split('_')[0] in [m.split('_')[0] for m in mansions]:
                         return position, degree, element
         else:
             if start <= ecl_lon < end:
                 degree = ecl_lon - start
                 for element, mansions in elements.items():
                     if position.split('_')[0] in [m.split('_')[0] for m in mansions]:
                         return position, degree, element
     return 'Unknown', 0, 'unknown'


def zodiac_sign_to_starting_degree(zodiac_sign):
    """
    将黄道十二星座转换为相对应的起始度数（英文）。
    """
    zodiac_degrees = {
        "Aries": 0,
        "Taurus": 30,
        "Gemini": 60,
        "Cancer": 90,
        "Leo": 120,
        "Virgo": 150,
        "Libra": 180,
        "Scorpio": 210,
        "Sagittarius": 240,
        "Capricorn": 270,
        "Aquarius": 300,
        "Pisces": 330
    }
    return zodiac_degrees.get(zodiac_sign, 0)

# 初始化列表以存储所有数据
all_data = []

# 定义行星及其对应的 swisseph 常量
planets = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN
}

# 定义需要比较的数值列名（小写）
numerical_columns_to_compare = [
    'year_degree', 'life_degree', 'sun_elong', 'moon_elong', 'mercury_elong', 'venus_elong',
    'mars_elong', 'saturn_elong', 'jupiter_elong', 'lilith_elong', 'selena_elong',
    'moon_south_node_elong', 'moon_north_node_elong', 'asc', 'mc', 'part_of_fortune'
]

# 定义五行元素映射（繁体中文）
elements_dict = {
    '旺': 'unknown',
    '相': 'unknown',
    '休': 'unknown',
    '囚': 'unknown',
    '死': 'unknown'
}

# 循环处理每一行数据
for idx, row in tqdm(readdata1.iterrows(), total=readdata1.shape[0], desc="Generating data"):
    utc_date = row["datetime"]  # 已经是时区感知的 datetime 对象
    jd = swe.julday(
        utc_date.year, utc_date.month, utc_date.day,
        utc_date.hour + utc_date.minute / 60.0 + utc_date.second / 3600.0
    )

    # 获取农历数据
    datetime_obj_shanghai = utc_date.astimezone(timezone(timedelta(hours=8))).replace(tzinfo=None)
    a = cnlunar.Lunar(datetime_obj_shanghai, godType='8char')

    # 提取八字四柱
    year_pillar = a.year8Char  # e.g., '甲子'
    month_pillar = a.month8Char
    day_pillar = a.day8Char
    hour_pillar = a.twohour8Char

    # 获取年、月、日、时四柱的天干和地支
    year_heavenly_stem = year_pillar[0]
    year_earthly_branch = year_pillar[-1]
    month_heavenly_stem = month_pillar[0]
    month_earthly_branch = month_pillar[-1]
    day_heavenly_stem = day_pillar[0]
    day_earthly_branch = day_pillar[-1]
    hour_heavenly_stem = hour_pillar[0]
    hour_earthly_branch = hour_pillar[-1]

    # 映射五行及阴阳（英文表示）
    year_element = heavenly_stems_mapping.get(year_heavenly_stem, {}).get('element', 'unknown')
    year_yin_yang = heavenly_stems_mapping.get(year_heavenly_stem, {}).get('yin_yang', 'unknown')
    month_element = heavenly_stems_mapping.get(month_heavenly_stem, {}).get('element', 'unknown')
    month_yin_yang = heavenly_stems_mapping.get(month_heavenly_stem, {}).get('yin_yang', 'unknown')
    day_element = heavenly_stems_mapping.get(day_heavenly_stem, {}).get('element', 'unknown')
    day_yin_yang = heavenly_stems_mapping.get(day_heavenly_stem, {}).get('yin_yang', 'unknown')
    hour_element = heavenly_stems_mapping.get(hour_heavenly_stem, {}).get('element', 'unknown')
    hour_yin_yang = heavenly_stems_mapping.get(hour_heavenly_stem, {}).get('yin_yang', 'unknown')

    # 获取四柱的纳音五行（英文）
    year_pillar_nayin = nayin_elements_chinese.get(year_pillar, 'unknown')
    month_pillar_nayin = nayin_elements_chinese.get(month_pillar, 'unknown')
    day_pillar_nayin = nayin_elements_chinese.get(day_pillar, 'unknown')
    hour_pillar_nayin = nayin_elements_chinese.get(hour_pillar, 'unknown')

    # 获取分柱（minute pillar）
    minute = datetime_obj_shanghai.minute  # 0-59
    mapped_minute = minute
    minute_pillar_stem, minute_pillar_branch = minute_pillar_mapping[mapped_minute]
    minute_pillar = f"{minute_pillar_stem}{minute_pillar_branch}"

    # 获取分柱的纳音五行（英文）
    minute_pillar_nayin = nayin_elements_chinese.get(minute_pillar, 'unknown')

    # 获取四柱的十二長生
    year_pillar_changsheng = changsheng_mapping.get((year_heavenly_stem, year_earthly_branch), 'unknown')
    month_pillar_changsheng = changsheng_mapping.get((month_heavenly_stem, month_earthly_branch), 'unknown')
    day_pillar_changsheng = changsheng_mapping.get((day_heavenly_stem, day_earthly_branch), 'unknown')
    hour_pillar_changsheng = changsheng_mapping.get((hour_heavenly_stem, hour_earthly_branch), 'unknown')
    minute_pillar_changsheng = changsheng_mapping.get((minute_pillar_stem, minute_pillar_branch), 'unknown')


    # 计算年限度数和对应的五行
    year_degree, year_degree_wuxing = calculate_year_degree(
        year_pillar, a.lunarYear, a.lunarMonth, a.lunarDay, a.isLunarLeapMonth
    )

    # 调试输出
    print(f"Year Pillar: '{year_pillar}', Nayin Element: '{year_degree_wuxing}'")


    # 计算上升点（asc）和中天点（mc）
    ascendant, midheaven, descendant, imum_coeli, equ_ascendant = calc_asc_mc(jd, latitude, longitude)

    # 计算行星数据
    planet_data = {}
    sun_elong = None

    for name, planet in planets.items():
        ecl_pos = swe.calc_ut(jd, planet)
        # ecl_pos 是一个元组： (longitude, latitude, distance, speed)
        elong = ecl_pos[0][0] % 360  # 黄经
        elat = ecl_pos[0][1]         # 黄纬
        distance = ecl_pos[0][2]     # 距离
        speed = ecl_pos[0][3]        # 速度

        planet_data.update({
            f"{name}_elong": elong,
            f"{name}_elat": elat,
            f"{name}_distance_au": distance,
            f"{name}_speed": speed
        })

        if name == "sun":
            sun_elong = elong

    # 计算速度类型
    speed_thresholds = {
        "stationary": 0.001,
        "slow": 0.5,
        "fast": 1.5,
    }

    for name in ["mercury", "venus", "mars", "jupiter", "saturn"]:
        elong = planet_data.get(f"{name}_elong", None)
        if elong is None:
            planet_data[f"{name}_speed_type"] = "unknown"
            continue
        elong_diff = abs(sun_elong - elong)
        elong_diff = min(elong_diff, 360 - elong_diff)
        if elong_diff <= 4:
            speed_type = "speed_invisible"  # 伏
        else:
            speed = planet_data.get(f"{name}_speed", None)
            if speed is None:
                speed_type = "unknown"
            else:
                if speed < 0:
                    speed_type = "speed_retrogade"
                else:
                    speed_abs = abs(speed)
                    if speed_abs < speed_thresholds["stationary"]:
                        speed_type = "speed_stationary"  # 留
                    elif speed_abs < speed_thresholds["slow"]:
                        speed_type = "speed_slow"  # 遲
                    elif speed_abs > speed_thresholds["fast"]:
                        speed_type = "speed_fast"  # 速
                    else:
                        speed_type = "speed_normal"  # 順
        planet_data[f"{name}_speed_type"] = speed_type

    # 计算福德点（part_of_fortune）
    moon_long = planet_data.get("moon_elong", None)
    if moon_long is None:
        fortune_long = None
    else:
        fortune_long = calculate_fortune(
            ascendant, sun_elong, moon_long, jd, latitude, longitude
        )

    # 如果 fortune_long 为 None，赋予一个默认值（如 0）
    if fortune_long is None:
        fortune_long = 0  # 或者其他合适的默认值

    # 调试输出
    print(f"Row {idx}: Fortune Long = {fortune_long}")


    # 计算月交点和莉莉丝
    moon_nodes = swe.calc_ut(jd, swe.MEAN_NODE)
    mean_lilith = swe.calc_ut(jd, swe.MEAN_APOG)

    # 正确提取黄经值
    moon_north_node_lon = moon_nodes[0][0] % 360 if moon_nodes and len(moon_nodes[0]) > 0 else None
    moon_south_node_lon = (moon_north_node_lon + 180) % 360 if moon_north_node_lon is not None else None
    mean_lilith_lon = mean_lilith[0][0] % 360 if mean_lilith and len(mean_lilith[0]) > 0 else None

    # 计算紫气（selena）
    purple_period = 10227.1792
    purple_base_date = pd.Timestamp('1975-03-13 16:00:00', tz='UTC')
    purple_base_degree = 230.5

    # 计算紫气位置
    time_difference = (utc_date - purple_base_date).total_seconds() / 86400
    completed_cycles = time_difference / purple_period
    remaining_cycles = completed_cycles - int(completed_cycles)
    remaining_days = remaining_cycles * purple_period
    degrees_per_day = 360 / purple_period
    degrees_difference = remaining_days * degrees_per_day
    selena_long = (purple_base_degree + degrees_difference) % 360

    # 获取农历月份对应的五行元素（英文）
    lunar_month = a.lunarMonth
    lunar_month_elements = {
        1: {'旺': 'wood', '相': 'fire', '休': 'water', '囚': 'metal', '死': 'earth'},
        2: {'旺': 'wood', '相': 'fire', '休': 'water', '囚': 'metal', '死': 'earth'},
        3: {'旺': 'earth', '相': 'metal', '休': 'fire', '囚': 'wood', '死': 'water'},
        4: {'旺': 'fire', '相': 'earth', '休': 'wood', '囚': 'water', '死': 'metal'},
        5: {'旺': 'fire', '相': 'earth', '休': 'wood', '囚': 'water', '死': 'metal'},
        6: {'旺': 'earth', '相': 'metal', '休': 'fire', '囚': 'wood', '死': 'water'},
        7: {'旺': 'metal', '相': 'water', '休': 'earth', '囚': 'fire', '死': 'wood'},
        8: {'旺': 'metal', '相': 'water', '休': 'earth', '囚': 'fire', '死': 'wood'},
        9: {'旺': 'earth', '相': 'metal', '休': 'fire', '囚': 'wood', '死': 'water'},
        10: {'旺': 'water', '相': 'wood', '休': 'metal', '囚': 'earth', '死': 'fire'},
        11: {'旺': 'water', '相': 'wood', '休': 'metal', '囚': 'earth', '死': 'fire'},
        12: {'旺': 'earth', '相': 'metal', '休': 'fire', '囚': 'wood', '死': 'water'}
    }
    if lunar_month in lunar_month_elements:
        elements_dict = lunar_month_elements[lunar_month]
    else:
        elements_dict = {'旺': 'unknown', '相': 'unknown', '休': 'unknown', '囚': 'unknown', '死': 'unknown'}

    # 计算分柱（minute pillar）
    minute = datetime_obj_shanghai.minute  # 0-59
    # 直接使用分钟值，不需要映射到60
    mapped_minute = minute
    minute_pillar_stem, minute_pillar_branch = minute_pillar_mapping[mapped_minute]
    minute_pillar = f"{minute_pillar_stem}{minute_pillar_branch}"

    # 映射五行及阴阳（英文表示）
    minute_element_stem = heavenly_stems_mapping.get(minute_pillar_stem, {}).get('element', 'unknown')
    minute_yin_yang_stem = heavenly_stems_mapping.get(minute_pillar_stem, {}).get('yin_yang', 'unknown')
    minute_element_branch = earthly_branches_mapping.get(minute_pillar_branch, {}).get('element', 'unknown')
    minute_yin_yang_branch = earthly_branches_mapping.get(minute_pillar_branch, {}).get('yin_yang', 'unknown')

    # 综合五行和阴阳
    minute_element = minute_element_stem  # 或根据需要综合
    minute_yin_yang = minute_yin_yang_stem  # 或根据需要综合

    # 获取分柱的十二長生
    minute_pillar_changsheng = changsheng_mapping.get((minute_pillar_stem, minute_pillar_branch), 'unknown')

    # 获取分柱地支五行及阴阳
    minute_earthly_branch = minute_pillar_branch
    minute_earthly_element = earthly_branches_mapping.get(minute_earthly_branch, {}).get('element', 'unknown')
    minute_earthly_yin_yang = earthly_branches_mapping.get(minute_earthly_branch, {}).get('yin_yang', 'unknown')

    # 获取年柱地支五行及阴阳
    year_earthly_element = earthly_branches_mapping.get(year_earthly_branch, {}).get('element', 'unknown')
    year_earthly_yin_yang = earthly_branches_mapping.get(year_earthly_branch, {}).get('yin_yang', 'unknown')

    # 获取月柱地支五行及阴阳
    month_earthly_element = earthly_branches_mapping.get(month_earthly_branch, {}).get('element', 'unknown')
    month_earthly_yin_yang = earthly_branches_mapping.get(month_earthly_branch, {}).get('yin_yang', 'unknown')

    # 获取日柱地支五行及阴阳
    day_earthly_element = earthly_branches_mapping.get(day_earthly_branch, {}).get('element', 'unknown')
    day_earthly_yin_yang = earthly_branches_mapping.get(day_earthly_branch, {}).get('yin_yang', 'unknown')

    # 获取时柱地支五行及阴阳
    hour_earthly_element = earthly_branches_mapping.get(hour_earthly_branch, {}).get('element', 'unknown')
    hour_earthly_yin_yang = earthly_branches_mapping.get(hour_earthly_branch, {}).get('yin_yang', 'unknown')

    # 编译所有数据
    single_row_data = {
        'datetime(utc)': utc_date,
        'datetime(utc+8)': datetime_obj_shanghai,
        'price': row['value'],
        'type': row['type'],
        '農曆數字': f"{a.lunarYear}-{a.lunarMonth}-{a.lunarDay}" + ('-閏' if a.isLunarLeapMonth else ''),
        '農曆年份': a.lunarYear,
        '農曆月份': a.lunarMonth,
        '農曆日子': a.lunarDay,
        '八字': ' '.join([year_pillar, month_pillar, day_pillar, hour_pillar]),  # 添加八字
        'chinese_solar_terms': solar_terms(ecl_lon=planet_data["sun_elong"]),
        '旺': elements_dict['旺'],
        '相': elements_dict['相'],
        '休': elements_dict['休'],
        '囚': elements_dict['囚'],
        '死': elements_dict['死'],
        '年柱': year_pillar,
        '年柱天干五行': year_element,
        '年柱天干陰陽': year_yin_yang,
        '年柱十二長生': year_pillar_changsheng,
        '年柱地支五行': year_earthly_element,
        '年柱地支陰陽': year_earthly_yin_yang,
        '年柱納音五行':year_pillar_nayin,
        '月柱': month_pillar,
        '月柱天干五行': month_element,
        '月柱天干陰陽': month_yin_yang,
        '月柱十二長生': month_pillar_changsheng,
        '月柱地支五行': month_earthly_element,
        '月柱地支陰陽': month_earthly_yin_yang,
        '月柱納音五行':month_pillar_nayin,
        '日柱': day_pillar,
        '日柱天干五行': day_element,
        '日柱天干陰陽': day_yin_yang,
        '日柱十二長生': day_pillar_changsheng,
        '日柱地支五行': day_earthly_element,
        '日柱地支陰陽': day_earthly_yin_yang,
        '日柱納音五行':day_pillar_nayin,
        '時柱': hour_pillar,
        '時柱天干五行': hour_element,
        '時柱天干陰陽': hour_yin_yang,
        '時柱十二長生': hour_pillar_changsheng,
        '時柱地支五行': hour_earthly_element,
        '時柱地支陰陽': hour_earthly_yin_yang,
        '時柱納音五行': hour_pillar_nayin,
        '分柱': minute_pillar,
        '分柱天干五行': minute_element,
        '分柱天干陰陽': minute_yin_yang,
        '分柱十二長生': minute_pillar_changsheng,
        '分柱地支五行': minute_earthly_element,
        '分柱地支陰陽': minute_earthly_yin_yang,
        '分柱納音五行': minute_pillar_nayin,
        'year_degree': year_degree,
        'year_degree_wuxing': year_degree_wuxing,  # 添加 year_degree_wuxing
        'part_of_fortune': fortune_long,
        'moon_north_node_elong': moon_north_node_lon,
        'moon_south_node_elong': moon_south_node_lon,
        'lilith_elong': mean_lilith_lon,
        'selena_elong': selena_long,
        'asc': ascendant,
        'mc': midheaven
    }
    single_row_data.update(planet_data)
    all_data.append(single_row_data)

# 将所有数据转换为 DataFrame
all_data_df = pd.DataFrame(all_data)

all_data_df['part_of_fortune'] = all_data_df['part_of_fortune'].fillna(0)

 # 添加星座和宿位信息
planet_positions = {
    'sun': 'sun_elong',
    'moon': 'moon_elong',
    'mars': 'mars_elong',
    'mercury': 'mercury_elong',
    'jupiter': 'jupiter_elong',
    'venus': 'venus_elong',
    'saturn': 'saturn_elong',
}

# 添加星座和宿位信息
for planet, pos in planet_positions.items():
    # 检查位置列是否存在
    if pos not in all_data_df.columns:
        print(f"警告：列 '{pos}' 不存在於 DataFrame 中。")
        continue
    # 添加星座信息
    all_data_df[[f"{planet}_elong_zodiac_signs", f"{planet}_elong_zodiac_sign_element", f"{planet}_elong_zodiac_degree"]] = all_data_df[pos].apply(
        lambda x: pd.Series(zodiac_sign(x) if pd.notna(x) else ('Unknown', 'unknown', 0))
    )
    # 添加宿位信息
    all_data_df[[f"{planet}_elong_mansion_positions", f"{planet}_elong_mansion_degree", f"{planet}_elong_mansion_element"]] = all_data_df[pos].apply(
        lambda x: pd.Series(mansion_position(x) if pd.notna(x) else ('Unknown', 0, 'unknown'))
    )

# 计算 Life_sign 和 Life_degree
if 'asc_zodiac_signs' in all_data_df.columns and 'sun_elong_zodiac_degree' in all_data_df.columns:
    all_data_df['life_sign'] = all_data_df['asc_zodiac_signs']
    all_data_df['life_sign_degree'] = all_data_df['sun_elong_zodiac_degree']
    all_data_df['life_degree'] = all_data_df['life_sign'].apply(zodiac_sign_to_starting_degree) + all_data_df['life_sign_degree']
else:
    print("警告：缺少 'asc_zodiac_signs' 或 'sun_elong_zodiac_degree' 列，无法计算 'life_sign' 和 'life_degree'。")
    all_data_df['life_sign'] = None
    all_data_df['life_sign_degree'] = None
    all_data_df['life_degree'] = None

# 定义特殊位置（如月交点、莉莉丝、上升点等）
special_positions = {
    'moon_north_node_elong': 'moon_north_node_elong',
    'moon_south_node_elong': 'moon_south_node_elong',
    'lilith_elong': 'lilith_elong',
    'selena_elong': 'selena_elong',
    'asc': 'asc',
    'mc': 'mc',
    'year_degree': 'year_degree',
    'part_of_fortune': 'part_of_fortune'
}

for item, pos in special_positions.items():
    # 检查位置列是否存在
    if pos not in all_data_df.columns:
        print(f"警告：列 '{pos}' 不存在於 DataFrame 中。")
        continue
    # 添加星座信息
    all_data_df[[f"{item}_zodiac_signs", f"{item}_zodiac_sign_element", f"{item}_zodiac_degree"]] = all_data_df[pos].apply(
        lambda x: pd.Series(zodiac_sign(x))
    )
    # 添加宿位信息
    all_data_df[[f"{item}_mansion_positions", f"{item}_mansion_degree", f"{item}_mansion_element"]] = all_data_df[pos].apply(
        lambda x: pd.Series(mansion_position(x))
    )

# 计算 Life_sign 和 Life_degree
if 'asc_zodiac_signs' in all_data_df.columns and 'sun_elong_zodiac_degree' in all_data_df.columns:
    all_data_df['life_sign'] = all_data_df['asc_zodiac_signs']
    all_data_df['life_sign_degree'] = all_data_df['sun_elong_zodiac_degree']
    all_data_df['life_degree'] = all_data_df['life_sign'].apply(zodiac_sign_to_starting_degree) + all_data_df['life_sign_degree']
else:
    print("警告：缺少 'asc_zodiac_signs' 或 'sun_elong_zodiac_degree' 列，无法计算 'life_sign' 和 'life_degree'。")
    all_data_df['life_sign'] = None
    all_data_df['life_sign_degree'] = None
    all_data_df['life_degree'] = None

# 导出第一个 DataFrame 到 CSV 文件
export_input_path = "/Users/jacky/Desktop/UltimateData/EXPORT_ALL_DATA_Y2006to2023_G8.csv"
try:
    all_data_df.to_csv(export_input_path, index=False, encoding='utf-8-sig')
    print(f"資料生成完成，已保存到 '{export_input_path}'")
except PermissionError:
    print(f"錯誤：無法寫入文件 '{export_input_path}'。請檢查文件路徑和寫入權限。")
    exit(1)
except Exception as e:
    print(f"保存 CSV 文件時發生錯誤：{e}")
    exit(1)

# ======================== Part 2: 数据处理 ========================

# 更新 CSV 文件路径
input_path = export_input_path
output_path = '/Users/jacky/Desktop/UltimateData/aspects_results_2006to2023_v18.csv'

# 读取 CSV 文件，包含错误处理
try:
    df = pd.read_csv(input_path)
    print("CSV 文件读取成功。")
except FileNotFoundError:
    print(f"錯誤：CSV 文件未找到於 {input_path}")
    exit(1)
except Exception as e:
    print(f"讀取 CSV 文件時發生錯誤：{e}")
    exit(1)

# 定义角度
angles = [0, 30, 45, 60, 90, 120, 144, 150, 180, 240, 270, 300, 330]

# 月相容差
moon_phase_tolerance = 3

# 需要比较的数值列名（小写）
numerical_columns_to_compare = [
    'year_degree', 'life_degree', 'sun_elong', 'moon_elong', 'mercury_elong', 'venus_elong',
    'mars_elong', 'saturn_elong', 'jupiter_elong', 'lilith_elong', 'selena_elong',
    'moon_south_node_elong', 'moon_north_node_elong', 'asc', 'mc', 'part_of_fortune'
]

# 餘奴所需的字符串列名（繁体中文）
string_columns_to_compare = [
    '旺', '相', '休', '囚', '死',
    'mars_elong_mansion_positions', 'mars_elong_zodiac_signs',
    'saturn_elong_mansion_positions', 'saturn_elong_zodiac_signs',
    'mercury_elong_mansion_positions', 'mercury_elong_zodiac_signs',
    'jupiter_elong_mansion_positions', 'jupiter_elong_zodiac_signs',
    'moon_south_node_elong_mansion_positions', 'moon_south_node_elong_zodiac_signs',
    'moon_north_node_elong_mansion_positions', 'moon_north_node_elong_zodiac_signs',
    'lilith_elong_mansion_positions', 'lilith_elong_zodiac_signs',
    'selena_elong_mansion_positions', 'selena_elong_zodiac_signs'
]

# 定义餘奴条件（繁体中文）
yunu_definitions = [
    ('lilith_elong', 'mercury_elong', 'water', "餘奴護主", "餘奴犯主"),
    ('moon_north_node_elong', 'saturn_elong', 'earth', "餘奴護主", "餘奴犯主"),
    ('moon_south_node_elong', 'mars_elong', 'fire', "餘奴護主", "餘奴犯主"),
    ('selena_elong', 'jupiter_elong', 'wood', "餘奴護主", "餘奴犯主")
]

# 初始化结果字典
results = defaultdict(dict)  # 用于存储最终计数和月相
aspects_counts = defaultdict(lambda: defaultdict(int))  # time_key -> aspect_key -> aspect_count
conjunction_counts = defaultdict(lambda: defaultdict(int))  # time_key -> aspect_key -> conjunction_count
yunu_guard_counts = defaultdict(lambda: defaultdict(int))  # time_key -> element -> guard_count
yunu_offend_counts = defaultdict(lambda: defaultdict(int))  # time_key -> element -> offend_count

# 定义容差
tolerance = 2

# 定义元素（包括 metal）
elements = ["water", "earth", "fire", "wood", "metal"]

# 定义一个函数来检查差异是否在角度容差范围内
def check_aspect(difference, angle, tolerance):
    angle_tolerance = 4 if angle == 0 else tolerance
    return (angle - angle_tolerance) <= difference <= (angle + angle_tolerance)

# 获取所有可能的 aspect_keys
aspect_keys = []
for birth_col in numerical_columns_to_compare:
    for current_col in numerical_columns_to_compare:
        if birth_col != current_col:
            aspect_key = f"birth_{birth_col}_vs_current_{current_col}"
            aspect_keys.append(aspect_key)

# 收集所有的 time_keys
time_keys = df['datetime(utc)'].unique().tolist()

# 初始化 results 中的所有 time_keys
for time_key in time_keys:
    results[time_key] = {}

# 遍历 DataFrame 行，显示进度条
for i, current_row in tqdm(df.iterrows(), total=df.shape[0], desc="Processing rows"):
    time_key = current_row['datetime(utc)']

    # 计算月相
    try:
        moon_sun_aspect_difference = current_row['moon_elong'] - current_row['sun_elong']
    except KeyError:
        moon_sun_aspect_difference = None

    moon_phase = "NA"

    if pd.notna(moon_sun_aspect_difference):
        if -moon_phase_tolerance <= moon_sun_aspect_difference <= moon_phase_tolerance:
            moon_phase = "新月_朔月"
        elif 45 - moon_phase_tolerance <= moon_sun_aspect_difference <= 45 + moon_phase_tolerance:
            moon_phase = "眉月_Waxing Crescent"
        elif 90 - moon_phase_tolerance <= moon_sun_aspect_difference <= 90 + moon_phase_tolerance:
            moon_phase = "上弦月_First Quarter"
        elif 135 - moon_phase_tolerance <= moon_sun_aspect_difference <= 135 + moon_phase_tolerance:
            moon_phase = "上凸月_Waxing Gibbous"
        elif 180 - moon_phase_tolerance <= moon_sun_aspect_difference <= 180 + moon_phase_tolerance:
            moon_phase = "滿月_Full Moon"
        elif -180 - moon_phase_tolerance <= moon_sun_aspect_difference <= -180 + moon_phase_tolerance:
            moon_phase = "下凸月_Waning Gibbous"
        elif -90 - moon_phase_tolerance <= moon_sun_aspect_difference <= -90 + moon_phase_tolerance:
            moon_phase = "下弦月_Last Quarter"
        elif -45 - moon_phase_tolerance <= moon_sun_aspect_difference <= -45 + moon_phase_tolerance:
            moon_phase = "殘月_Waning Crescent"

    results[time_key]["moon_phase"] = moon_phase

    # 处理 aspects
    for birth_col in numerical_columns_to_compare:
        for current_col in numerical_columns_to_compare:
            if birth_col == current_col:
                continue  # 跳过相同列比较

            # 获取出生图的度数
            try:
                birth_value = current_row[birth_col]
            except KeyError:
                birth_value = None

            if pd.isna(birth_value):
                continue  # 如果没有找到对应时间的出生值，跳过

            current_value = current_row[current_col]

            if pd.isna(current_value):
                continue  # 如果当前值为NaN，跳过

            difference = abs(birth_value - current_value) % 360
            if difference > 180:
                difference = 360 - difference

            aspect_key = f"birth_{birth_col}_vs_current_{current_col}"
            for angle in angles:
                if check_aspect(difference, angle, tolerance):
                    if angle == 0:
                        # Conjunction count
                        conjunction_counts[time_key][aspect_key] += 1
                    else:
                        # Aspect count
                        aspects_counts[time_key][aspect_key] += 1

    # 处理餘奴 (yunu)
    yunu_results = defaultdict(lambda: {"guard": 0, "offend": 0})

    for birth_col, current_col, element, yunu_guard, yunu_offend in yunu_definitions:
        if birth_col not in numerical_columns_to_compare or current_col not in numerical_columns_to_compare:
            continue  # 确保列存在于比较列表中

        # 计算差异
        birth_value = current_row.get(birth_col, None)
        current_value = current_row.get(current_col, None)

        if pd.isna(birth_value) or pd.isna(current_value):
            continue  # 如果任何一个值为NaN，跳过

        birth_difference = abs(birth_value - current_value) % 360
        if birth_difference > 180:
            birth_difference = 360 - birth_difference

        current_difference = abs(current_row.get(birth_col, 0) - current_row.get(current_col, 0)) % 360
        if current_difference > 180:
            current_difference = 360 - current_difference

        # 本命 vs 流年 = birth_difference, 'birth'; 流年 vs 流年 = current_difference, 'current'
        for difference in [birth_difference, current_difference]:
            for angle in angles:
                if check_aspect(difference, angle, tolerance):
                    if pd.notna(current_row['旺']) and str(current_row['旺']).strip().lower() == element.lower():
                        yunu_results[element]['guard'] += 1
                    else:
                        yunu_results[element]['offend'] += 1

        # 检查 Mansion_positions
        mansion_positions_conditions = [
            (current_row.get(f'{birth_col}_mansion_positions', ""), current_row.get(f'{current_col}_mansion_positions', "")),
            (current_row.get(f'{current_col}_mansion_positions', ""), current_row.get(f'{birth_col}_mansion_positions', ""))
        ]

        for b_mansion, c_mansion in mansion_positions_conditions:
            if pd.notna(b_mansion) and pd.notna(c_mansion) and b_mansion == c_mansion:
                if pd.notna(current_row['旺']) and str(current_row['旺']).strip().lower() == element.lower():
                    yunu_results[element]['guard'] += 1
                else:
                    yunu_results[element]['offend'] += 1

        # 检查 Zodiac_signs
        zodiac_signs_conditions = [
            (current_row.get(f'{birth_col}_zodiac_signs', ""), current_row.get(f'{current_col}_zodiac_signs', "")),
            (current_row.get(f'{current_col}_zodiac_signs', ""), current_row.get(f'{birth_col}_zodiac_signs', ""))
        ]

        for b_zodiac, c_zodiac in zodiac_signs_conditions:
            if pd.notna(b_zodiac) and pd.notna(c_zodiac) and b_zodiac == c_zodiac:
                if pd.notna(current_row['旺']) and str(current_row['旺']).strip().lower() == element.lower():
                    yunu_results[element]['guard'] += 1
                else:
                    yunu_results[element]['offend'] += 1

    # 更新 yunu 计数
    for element in elements:
        y_guard = yunu_results[element]['guard']
        y_offend = yunu_results[element]['offend']
        yunu_guard_counts[time_key][element] = y_guard
        yunu_offend_counts[time_key][element] = y_offend

    # 确保每个元素都有记录，即使是0
    for element in elements:
        if element not in yunu_results:
            yunu_guard_counts[time_key][element] = 0
            yunu_offend_counts[time_key][element] = 0

    # 获取当前行的五柱地支五行及阴阳信息
    # 年柱地支五行及阴阳
    year_earthly_branch = current_row['年柱'][-1]  # 假设 '年柱' 格式为 '甲子'
    year_pillar_earthly_element = earthly_branches_mapping.get(year_earthly_branch, {}).get('element', 'unknown')
    year_pillar_earthly_yin_yang = earthly_branches_mapping.get(year_earthly_branch, {}).get('yin_yang', 'unknown')

    # 月柱地支五行及阴阳
    month_earthly_branch = current_row['月柱'][-1]
    month_pillar_earthly_element = earthly_branches_mapping.get(month_earthly_branch, {}).get('element', 'unknown')
    month_pillar_earthly_yin_yang = earthly_branches_mapping.get(month_earthly_branch, {}).get('yin_yang', 'unknown')

    # 日柱地支五行及阴阳
    day_earthly_branch = current_row['日柱'][-1]
    day_pillar_earthly_element = earthly_branches_mapping.get(day_earthly_branch, {}).get('element', 'unknown')
    day_pillar_earthly_yin_yang = earthly_branches_mapping.get(day_earthly_branch, {}).get('yin_yang', 'unknown')

    # 時柱地支五行及陰陽
    hour_earthly_branch = current_row['時柱'][-1]
    hour_pillar_earthly_element = earthly_branches_mapping.get(hour_earthly_branch, {}).get('element', 'unknown')
    hour_pillar_earthly_yin_yang = earthly_branches_mapping.get(hour_earthly_branch, {}).get('yin_yang', 'unknown')

    # 分柱地支五行及陰陽
    minute_earthly_branch = minute_pillar_branch
    minute_pillar_earthly_element = earthly_branches_mapping.get(minute_earthly_branch, {}).get('element', 'unknown')
    minute_pillar_earthly_yin_yang = earthly_branches_mapping.get(minute_earthly_branch, {}).get('yin_yang', 'unknown')

    # 更新结果字典中的地支五行及阴阳信息
    results[time_key]['年柱地支五行'] = year_pillar_earthly_element
    results[time_key]['年柱地支陰陽'] = year_pillar_earthly_yin_yang

    results[time_key]['月柱地支五行'] = month_pillar_earthly_element
    results[time_key]['月柱地支陰陽'] = month_pillar_earthly_yin_yang

    results[time_key]['日柱地支五行'] = day_pillar_earthly_element
    results[time_key]['日柱地支陰陽'] = day_pillar_earthly_yin_yang

    results[time_key]['時柱地支五行'] = hour_pillar_earthly_element
    results[time_key]['時柱地支陰陽'] = hour_pillar_earthly_yin_yang

    results[time_key]['分柱地支五行'] = minute_pillar_earthly_element
    results[time_key]['分柱地支陰陽'] = minute_pillar_earthly_yin_yang

# 确保所有预期的列都存在于 results 中
for time_key in results.keys():
    # 添加 aspects 计数
    for aspect_key in aspect_keys:
        count = aspects_counts.get(time_key, {}).get(aspect_key, 0)
        results[time_key][f"{aspect_key}_aspect_count"] = count

    # 添加 conjunctions 计数
    for aspect_key in aspect_keys:
        count = conjunction_counts.get(time_key, {}).get(aspect_key, 0)
        results[time_key][f"{aspect_key}_conjunction_count"] = count

    # 添加 yunu 计数
    for element in elements:
        guard_count = yunu_guard_counts.get(time_key, {}).get(element, 0)
        offend_count = yunu_offend_counts.get(time_key, {}).get(element, 0)
        results[time_key][f"{element}_yunu_guard_count"] = guard_count
        results[time_key][f"{element}_yunu_offend_count"] = offend_count

# 将结果转换为 DataFrame
results_df = pd.DataFrame.from_dict(results, orient='index').reset_index()
results_df.rename(columns={'index': 'datetime(utc)'}, inplace=True)

# 将 'datetime(utc)' 转换为 datetime，处理错误
results_df['datetime(utc)'] = pd.to_datetime(results_df['datetime(utc)'], errors='coerce')
# 可选：移除無效的時間行
results_df = results_df.dropna(subset=['datetime(utc)'])

# 按照 datetime(utc) 列排序
results_df.sort_values(by='datetime(utc)', inplace=True)

# 定义列顺序：datetime 首先，然后是 aspects counts，接着是 conjunctions counts，最后是 yunu counts，包含其他列
column_order = [
    'datetime(utc)', 'datetime(utc+8)', 'price', 'type', '農曆數字',
    '農曆年份', '農曆月份', '農曆日子', '八字',
    'chinese_solar_terms', '旺', '相', '休', '囚', '死',
    '年柱', '年柱天干五行', '年柱天干陰陽', '年柱十二長生', '年柱地支五行', '年柱地支陰陽', '年柱納音五行',
    'year_degree', 'year_degree_wuxing',
    '月柱', '月柱天干五行', '月柱天干陰陽', '月柱十二長生', '月柱地支五行', '月柱地支陰陽','月柱納音五行',
    '日柱', '日柱天干五行', '日柱天干陰陽', '日柱十二長生', '日柱地支五行', '日柱地支陰陽','日柱納音五行',
    '時柱', '時柱天干五行', '時柱天干陰陽', '時柱十二長生', '時柱地支五行', '時柱地支陰陽','時柱納音五行',
    '分柱', '分柱天干五行', '分柱天干陰陽', '分柱十二長生', '分柱地支五行', '分柱地支陰陽','分柱納音五行',
    'asc', 'mc', 'part_of_fortune',
    'moon_north_node_elong', 'moon_south_node_elong', 'lilith_elong', 'selena_elong'
]

# 添加 aspects 计数
for aspect_key in aspect_keys:
    count_col = f"{aspect_key}_aspect_count"
    column_order.append(count_col)

# 添加 conjunctions 计数
for aspect_key in aspect_keys:
    count_col = f"{aspect_key}_conjunction_count"
    column_order.append(count_col)

# 添加 yunu 计数
for element in elements:
    column_order.append(f"{element}_yunu_guard_count")
    column_order.append(f"{element}_yunu_offend_count")

# 添加任何其他未被添加的列
for col in results_df.columns:
    if col not in column_order:
        column_order.append(col)

# 重新排序列
existing_columns = [col for col in column_order if col in results_df.columns]
results_df = results_df[existing_columns]

# 保存结果到 CSV 文件，包含错误处理
try:
    results_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"處理完成，結果已保存到 '{output_path}'")
except PermissionError:
    print(f"錯誤：無法寫入文件 '{output_path}'。請檢查文件路徑和寫入權限。")
except Exception as e:
    print(f"保存 CSV 文件時發生錯誤 ({output_path})：{e}")

# ======================== Part 3: 合併兩個 CSV 文件 ========================

# 定义输入文件路径
csv1_path = "/Users/jacky/Desktop/UltimateData/EXPORT_ALL_DATA_Y2006to2023_G8.csv"
csv2_path = "/Users/jacky/Desktop/UltimateData/aspects_results_2006to2023_v18.csv"

# 定义输出文件路径
merged_output_path = "/Users/jacky/Desktop/alldata_29.csv"

# 读取第一个 CSV 文件
try:
    df1 = pd.read_csv(csv1_path, parse_dates=['datetime(utc)'])
    print(f"成功读取 '{csv1_path}'")
except FileNotFoundError:
    print(f"錯誤：CSV 文件未找到於 {csv1_path}")
    exit(1)
except Exception as e:
    print(f"读取 CSV 文件时发生錯誤 ({csv1_path})：{e}")
    exit(1)

# 读取第二个 CSV 文件
try:
    df2 = pd.read_csv(csv2_path, parse_dates=['datetime(utc)'])
    print(f"成功读取 '{csv2_path}'")
except FileNotFoundError:
    print(f"錯誤：CSV 文件未找到於 {csv2_path}")
    exit(1)
except Exception as e:
    print(f"读取 CSV 文件时发生錯誤 ({csv2_path})：{e}")
    exit(1)

# 确保两个 DataFrame 都有 'datetime(utc)' 列
if 'datetime(utc)' not in df1.columns:
    print(f"錯誤：'{csv1_path}' 中缺少 'datetime(utc)' 列。")
    exit(1)

if 'datetime(utc)' not in df2.columns:
    print(f"錯誤：'{csv2_path}' 中缺少 'datetime(utc)' 列。")
    exit(1)

# 找出 df2 中与 df1 重叠的列（除了 'datetime(utc)'）
overlapping_columns = [col for col in df2.columns if col in df1.columns and col != 'datetime(utc)']

# 从 df2 中删除这些重叠的列
df2 = df2.drop(columns=overlapping_columns)

# 合并两个 DataFrame，基于 'datetime(utc)' 列
merged_df = pd.merge(df1, df2, on='datetime(utc)', how='inner')

# 检查合并后的 DataFrame 是否为空
if merged_df.empty:
    print("警告：合并后的 DataFrame 为空。请检查两个 CSV 文件中的 'datetime(utc)' 列是否有匹配的值。")
else:
    print(f"合并完成，合并后的资料包含 {merged_df.shape[0]} 行。")

# 导出合并后的 DataFrame 到新的 CSV 文件
try:
    merged_df.to_csv(merged_output_path, index=False, encoding='utf-8-sig')
    print(f"合并后的资料已保存到 '{merged_output_path}'")
except PermissionError:
    print(f"錯誤：無法寫入文件 '{merged_output_path}'。請檢查文件路徑和寫入權限。")
except Exception as e:
    print(f"保存 CSV 文件时发生錯誤 ({merged_output_path})：{e}")
