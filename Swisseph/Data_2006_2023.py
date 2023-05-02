import swisseph as swe
import math
from datetime import datetime, timezone, timedelta
import pytz
import numpy as np
import csv
import pandas as pd
import math
import cnlunar
from lunar_python import LunarYear

#from astropy.coordinates import SkyCoord, EarthLocation, BarycentricTrueEcliptic
readdata1 = pd.read_csv("/Users/jacky/Desktop/HSI/HSI_HL_2006to2023_updated.csv", header=None, skiprows=1, names=['DateTime', 'Value', 'Type'], encoding='ISO-8859-1')

# Convert time column to pandas datetime object
time_pd = pd.to_datetime(readdata1['DateTime'], format='%Y-%m-%d %H:%M:%S')

# Convert pandas datetime object to string format
time_str = time_pd.dt.strftime('%Y-%m-%d %H:%M:%S')

# Replace time column in data with string format
readdata1['DateTime'] = time_str

# Set GeoLat, GeoLon
latitude = 22.283875
longitude = 114.158229

# Create an empty DataFrame to store the data for all times
all_data = pd.DataFrame()

all_data['solar_term'] = None
all_data['Zodiac_signs'] = None
all_data['Zodiac_degree'] = None
all_data['Mansion_positions'] = None
all_data['Mansion_degree'] = None
all_data['Mansion_element']  = None
all_data['Astronomy_boundary'] = None
all_data['Astronomy_degree'] = None
all_data['life_sign'] = None
all_data['life_sign_degree'] = None
all_data['Year_Degree'] = None


# 循環處理每個從CSV輸入的時間
all_data = []
year_degrees = []

#洞微大限（只限HSI）
year_degrees = {
    "Year_2005": [230.216666667, 228.216666667],
    "Year_2006": [228.216666667, 226.216666667],
    "Year_2007": [226.216666667, 224.216666667],
    "Year_2008": [224.216666667, 222.216666667],
    "Year_2009": [222.216666667, 220.216666667],
    "Year_2010": [220.216666667, 218.216666667],
    "Year_2011": [218.216666667, 216.216666667],
    "Year_2012": [216.216666667, 214.216666667],
    "Year_2013": [214.216666667, 212.216666667],
    "Year_2014": [212.216666667, 210.216666667],
    "Year_2015": [210.216666667, 206.65],
    "Year_2016": [206.65, 202.883333333],
    "Year_2017": [202.883333333, 199.15],
    "Year_2018": [199.15, 195.4],
    "Year_2019": [195.4, 191.65],
    "Year_2020": [191.65, 187.883333333],
    "Year_2021": [187.883333333, 184.15],
    "Year_2022": [184.15, 180.4],
    "Year_2023": [180.4, 176.166666667]
    }


def calculate_year_degree(lunar_year, lunar_month, lunar_day, is_leap_month, year_degrees):
    year_key = f"Year_{lunar_year}"
    if year_key not in year_degrees:
        return 330

    lunarYear = LunarYear.fromYear(lunar_year)
    day_count = lunarYear.getDayCount()
    year_degree_range = year_degrees.get(year_key)

    start_degree, end_degree = year_degree_range
    day_index = 0

    for month_idx in range(1, lunar_month + 1):
        month = lunarYear.getMonth(month_idx)
        if month_idx == lunar_month:
            day_index += lunar_day
        else:
            day_index += month.getDayCount()

        if month_idx == lunar_month and is_leap_month and month.isLeap():
            day_index += month.getDayCount()

    return start_degree + (end_degree - start_degree) * (day_index - 1) / (day_count - 1)


for idx, row in readdata1.iterrows():

    time_pd = row["DateTime"]
    # 将日期字符串转换为 pandas.Timestamp 对象，并将其转换为 UTC 时间
    utc_date = pd.to_datetime(time_pd)
    #计算儒略日
    jd = swe.julday(utc_date.year, utc_date.month, utc_date.day, utc_date.hour + utc_date.minute / 60.0 + utc_date.second / 3600.0)
    
    
    #Chinese elements

    datetime_obj_utc = utc_date  # 將帶時區的日期轉換為不帶時區的日期
    datetime_obj_shanghai = utc_date.to_pydatetime().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))).replace(tzinfo=None)
    a = cnlunar.Lunar(datetime_obj_shanghai, godType='8char', year8Char='beginningOfSpring')
   

    single_row_data= ({
    'DateTime(UTC)': utc_date,  # 將原始UTC DateTime添加到字典
    'Datetime(UTC+8)': a.date,
    'Price': row['Value'],
    'Type': row['Type'],
    '農曆數字': (a.lunarYear, a.lunarMonth, a.lunarDay, '闰' if a.isLunarLeapMonth else ''),
    '農曆': '%s %s[%s]年 %s%s' % (a.lunarYearCn, a.year8Char, a.chineseYearZodiac, a.lunarMonthCn, a.lunarDayCn),
    '星期': a.weekDayCn,
    '纳音': a.get_nayin(),

    })

    year_degree = calculate_year_degree(a.lunarYear, a.lunarMonth, a.lunarDay, a.isLunarLeapMonth, year_degrees)

    single_row_data.update({
        'Year_Degree': year_degree,
    })


    def calc_asc_mc(latitude, longitude, utc_date):
        cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
        ascendant = ascmc[0]
        midheaven = ascmc[1]
        descendant = cusps[6]
        imum_coeli = cusps[3]
        equ_ascendant = ascmc[4]

        return ascendant, midheaven, descendant, imum_coeli, equ_ascendant
    
    ascendant, midheaven, descendant, imum_coeli, equ_ascendant = calc_asc_mc(latitude, longitude, utc_date)

    single_row_data.update({
        'Time': utc_date,
        'ASC':ascendant,
        'MC':midheaven,
        'DES': descendant,
        'IC': imum_coeli,
        'EQU_ASC' : equ_ascendant
        })
    
    # Define Planets
    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mercury": swe.MERCURY,
        "Venus": swe.VENUS,
        "Mars": swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "Uranus": swe. URANUS,
        "Neptune": swe.NEPTUNE,
        "Pluto": swe.PLUTO
    }

    #定義行星的速度 Define Planet's Speed
    speed_thresholds = {
    "STATIONARY": 0.1,
    "SLOW": 0.5,
    "FAST": 1.5,
    }


    def is_speed_eclipse(jd, name, planet):
        if name == "Sun":
            sun_lon, _ = swe.calc_ut(jd, swe.SUN)
            if planet == "Mercury":
                mercury_lon, _ = swe.calc_ut(jd, swe.MERCURY)
                if abs(sun_lon - mercury_lon) <= 4:
                    return True
            elif planet == "Venus":
                venus_lon, _ = swe.calc_ut(jd, swe.VENUS)
                if abs(sun_lon - venus_lon) <= 4:
                    return True
            elif planet == "Mars":
                mars_lon, _ = swe.calc_ut(jd, swe.MARS)
                if abs(sun_lon - mars_lon) <= 4:
                    return True
            elif planet == "Saturn":
                saturn_lon, _ = swe.calc_ut(jd, swe.SATURN)
                if abs(sun_lon - saturn_lon) <= 4:
                    return True
            elif planet == "Jupiter":
                jupiter_lon, _ = swe.calc_ut(jd, swe.JUPITER)
                if abs(sun_lon - jupiter_lon) <= 4:
                    return True
            return False
    
    #Speed 
    def get_speed_type(speed, jd, name, planet):
        if is_speed_eclipse(jd, name, planet):
            return "SPEED_ECLIPSE"
        elif speed < 0:
            return "SPEED_REVERSE"
        else:
            speed = abs(speed)
            if speed < speed_thresholds["STATIONARY"]:
                return "SPEED_STATIONARY"
            elif speed < speed_thresholds["SLOW"]:
                return "SPEED_SLOW"
            elif speed > speed_thresholds["FAST"]:
                return "SPEED_FAST"
            else:
                return "SPEED_NORMAL"


    # Calculate the planet's ecliptic and equatorial longitude and latitude 計算行星在黃道及赤道的經緯度
    iflag = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_EQUATORIAL

    for name, planet in planets.items():
        
        ecl_pos = swe.calc_ut(jd, planet)
        ecl_l, ecl_2 = ecl_pos[:2]

        elong = ecl_l[0]
        elat = ecl_l[1]
        distance = ecl_l[2]

        pos = swe.calc_ut(jd, planet, iflag)
        equ_1, equ_2 = pos[:2]

        ra = equ_1[0]
        dec = equ_1[1]

        speed = ecl_l[3]  # 提取行星速度

        speed_type = get_speed_type(speed, jd, name, planet)  # 获取行星速度类型

        single_row_data.update({
            f"{name}_SPEED": speed,
            f"{name}_SPEED_TYPE": speed_type,
            })

        single_row_data.update({
            f"{name}_ELONG": elong,
            f"{name}_ELAT": elat,
            f"{name}_RA": ra,
            f"{name}_DEC": dec,
            f"{name}_DISTANCE_AU": distance
            })

        #print(f"{name}_ELONG:", elong), print(f"{name}_ELAT:", elat),print(f"{name}_RA:", ra),print(f"{name}_DEC:", dec)

    sun_long = single_row_data["Sun_ELONG"]
    moon_long = single_row_data["Moon_ELONG"]
    
    def calculate_fortune(ascendant, sun_long, moon_long, utc_date, latitude, longitude):
        jd = swe.utc_to_jd(utc_date.year, utc_date.month, utc_date.day, utc_date.hour, utc_date.minute, utc_date.second, swe.GREG_CAL)[1]

        geopos = (longitude, latitude, 0)
        # Calculate sunrise and sunset times using swe_rise_trans
        rise_flags = swe.CALC_RISE | swe.BIT_DISC_CENTER
        set_flags = swe.CALC_SET | swe.BIT_DISC_CENTER
        atpress = 0
        attemp = 0
        flags = 0

    
        res_sunrise = swe.rise_trans(jd, swe.SUN, 0, rise_flags, *geopos)
        res_sunset = swe.rise_trans(jd, swe.SUN, 0, set_flags, *geopos)

        jd_sunrise = res_sunrise[1][0]
        jd_sunset = res_sunset[1][0]

        # Check if the current time is between sunrise and sunset
        is_daytime = jd_sunrise <= jd and jd < jd_sunset

        # Calculate fortune point based on daytime or nighttime
        if is_daytime:
            fortune_long = ascendant + moon_long - sun_long
        else:
            fortune_long = ascendant + sun_long - moon_long

        fortune_long = fortune_long % 360

        return fortune_long

    fortune_long = calculate_fortune(ascendant, sun_long, moon_long , utc_date, latitude, longitude)

    single_row_data.update({ "Part_of_Fortune": fortune_long })

    # Calculate Moon's South Node, North Node and Lilith (Moon's Apogee) 计算月球北交点、南交点和莉莉丝
    moon_nodes, ret = swe.calc_ut(jd, swe.MEAN_NODE)
    mean_lilith, ret = swe.calc_ut(jd, swe.MEAN_APOG)
    mean_lilith_lon = mean_lilith[0]
    mean_lilith_lat = mean_lilith[1]
    mean_lilith_dist = mean_lilith[2]


    moon_north_node_lon = moon_nodes[0]
    #moon_north_node_lat = moon_nodes[1]
    moon_south_node_lon = (moon_nodes[0] + 180) % 360
    #moon_south_node_lat = -moon_nodes[1]

    #EXTRA MOON TRUE NODE
    moon_true_node, ret, = swe.calc_ut(jd, swe.TRUE_NODE)
    true_node = moon_true_node [1]

    
    # The basic year of Selena 紫氣的基礎年份
    purple_period = 10227.1792
    purple_base_date = pd.Timestamp('1975-03-13 16:00:00', tz='UTC')
    purple_base_degree = 230.5

    # Define Selena‘s Cycle 定義紫氣的周期
    def calculate_purple_position(target_date, base_date, base_degree, period):
        time_difference = target_date - base_date
        days_difference = time_difference.total_seconds() / 86400
        completed_cycles = days_difference / period
        remaining_cycles = completed_cycles - int(completed_cycles)
        remaining_days = remaining_cycles * period
        degrees_per_day = 360 / period
        degrees_difference = remaining_days * degrees_per_day
        current_position = base_degree + degrees_difference
        current_position %= 360
        return current_position
    
    date = utc_date.tz_localize('UTC')
    purple_position = calculate_purple_position(date, purple_base_date, purple_base_degree, purple_period)
    selena_long = purple_position
    #selena_lat = 0  # Assume that Selena is on Ecliptic’s Latitude 假设 Selena 在黄道平面上
    #selena_ra, selena_dec = ecl2equ(jd, selena_long, selena_lat)

    single_row_data.update({
        "Moon_North_Node_ELONG": moon_north_node_lon,
        "Moon_South_Node_ELONG": moon_south_node_lon,
        "Lilith_ELONG": mean_lilith_lon,
        "Lilith_LAT": mean_lilith_lat,
        "Lilith_DIST": mean_lilith_dist,
        "Selena_ELONG": selena_long
        # "Selena_RA": selena_ra,
 
        })

    all_data.append(single_row_data) 

# 24 Solar Terms， Lunar Month and elements
    def solar_terms(ecl_lon):
            terms = [
        (315, 330, 'Beginning_of_Spring_立春_寅'),
        (330, 345, 'First_month_midpoint_雨水_寅'),
        (345, 360, 'Second_month_midpoint_驚蟄_卯'),
        (0, 15, 'Spring_Equinox_春分_卯'),
        (15, 30, 'First_april_清明_辰'),
        (30, 45, 'Second_april_穀雨_辰'),
        (45, 60, 'Beginning_of_Summer_立夏_巳'),
        (60, 75, 'First_month_midpoint_小滿_巳'),
        (75, 90, 'Second_month_midpoint_芒種_午'),
        (90, 105, 'Summer_Solstice_夏至_午'),
        (105, 120, 'First_july_小暑_未'),
        (120, 135, 'Second_july_大暑_未'),
        (135, 150, 'Beginning_of_Autumn_立秋_申'),
        (150, 165, 'First_month_midpoint_處暑_申'),
        (165, 180, 'Second_month_midpoint_白露_酉'),
        (180, 195, 'Autumn_Equinox_秋分_酉'),
        (195, 210, 'First_october_寒露_戌'),
        (210, 225, 'Second_october_霜降_戌'),
        (225, 240, 'Beginning_of_Winter_立冬_亥'),
        (240, 255, 'First_month_midpoint_小雪_亥'),
        (255, 270, 'Second_month_midpoint_大雪_子'),
        (270, 285, 'Winter_Solstice_冬至_子'),
        (285, 300, 'First_january_小寒_丑'),
        (300, 315, 'Second_january_大寒_丑'),
        ]
            elements_order = [
        ('Wood', 'Fire', 'Water', 'Metal', 'Earth'), 
        ('Wood', 'Fire', 'Water', 'Metal', 'Earth'),
        ('Wood', 'Fire', 'Water', 'Metal', 'Earth'),
        ('Wood', 'Fire', 'Water', 'Metal', 'Earth'),
        ('Earth', 'Metal', 'Fire', 'Wood', 'Water'),
	    ('Earth', 'Metal', 'Fire', 'Wood', 'Water'),
        ('Fire', 'Earth', 'Wood', 'Water', 'Metal'),
        ('Fire', 'Earth', 'Wood', 'Water', 'Metal'),
        ('Fire', 'Earth', 'Wood', 'Water', 'Metal'),
        ('Fire', 'Earth', 'Wood', 'Water', 'Metal'),
        ('Earth', 'Metal', 'Fire', 'Wood', 'Water'),
        ('Earth', 'Metal', 'Fire', 'Wood', 'Water'),
        ('Metal', 'Water', 'Earth', 'Fire', 'Wood'),
        ('Metal', 'Water', 'Earth', 'Fire', 'Wood'),
        ('Metal', 'Water', 'Earth', 'Fire', 'Wood'),
        ('Metal', 'Water', 'Earth', 'Fire', 'Wood'),
        ('Earth', 'Metal', 'Fire', 'Wood', 'Water'),
        ('Earth', 'Metal', 'Fire', 'Wood', 'Water'),
        ('Water', 'Wood', 'Metal', 'Earth', 'Fire'),
        ('Water', 'Wood', 'Metal', 'Earth', 'Fire'),
        ('Water', 'Wood', 'Metal', 'Earth', 'Fire'),
        ('Water', 'Wood', 'Metal', 'Earth', 'Fire'),
        ('Earth', 'Metal', 'Fire', 'Wood', 'Water'),
        ('Earth', 'Metal', 'Fire', 'Wood', 'Water')
        ]
            for i, (start, end, term) in enumerate(terms):
                if start > end:
                    if ecl_lon >= start or ecl_lon < end:
                        chinese_range = f"{start}_{end}"
                        chinese_term = term.split('_')[1]
                        chinese_month = term.split('_')[2]
                        elements = elements_order[i]
                        return chinese_range, chinese_term, chinese_month, elements
                else:
                    if ecl_lon >= start and ecl_lon < end:
                        chinese_range = f"{start}_{end}"
                        chinese_term = term.split('_')[1]
                        chinese_month = term.split('_')[2]
                        elements = elements_order[i]
                        return chinese_range, chinese_term, chinese_month, elements
            return None, None, None, None

# 12 Zodiac Signs in Western Astrology
    def zodiac_sign(ecl_lon):
            signs = {
        (0, 30): 'Aries_Fire', 
        (30, 60): 'Taurus_Metal', 
        (60, 90): 'Gemini_Water', 
        (90, 120): 'Cancer_Moon', 
        (120, 150): 'Leo_Sun', 
        (150, 180): 'Virgo_Water', 
        (180, 210): 'Libra_Metal', 
        (210, 240): 'Scorpio_Fire',
        (240, 270): 'Sagittarius_Wood', 
        (270, 300): 'Capricorn_Earth', 
        (300, 330): 'Aquarius_Earth', 
        (330, 360): 'Pisces_Wood' 
        }
            for (start, end), sign in signs.items():
                if start <= ecl_lon and ecl_lon < end:
                    degree = ecl_lon - start
                    split_sign = sign.split("_")
                    sign_name = split_sign[0]
                    sign_element = "_".join(split_sign[1:])
                    return pd.Series([sign_name, sign_element, degree])
            return None

#28 Mansions in Chinese Astrology    
    def mansion_position(ecl_lon):
            positions = {
        (203.8374893, 214.4898543): '角宿_Horn_Wood',
        (214.4898543, 225.0215638): '亢宿_Neck_Metal',
        (225.0215638, 242.9360091): '氐宿_Root_Earth',
        (242.9360091, 249.7584245): '房宿_Room_Sun_element',
        (249.7584245, 256.1517382): '心宿_Heart_Moon_element',
        (256.1517382, 271.2575671): '尾宿_Tail_Fire',
        (271.2575671, 280.1774751): '箕宿_Winnowing_Basket_Water',
        (280.1774751, 304.0435179): '斗宿_Dipper_Wood',
        (304.0435179, 311.7193257): '牛宿_Ox_Metal',
        (311.7193257, 323.3911983): '女宿_Girl_Earth',
        (323.3911983, 333.348599): '虚宿_Emptiness_Sun_element',
        (333.348599, 353.481734): '危宿_Rooftop_Moon_element',
        (353.481734, 359.9999999): '室宿0前_Encampment_Fire',
        (0, 9.152166707): '室宿0後_Encampment_Fire',
        (9.152166707, 22.37214699): '壁宿_Wail_Water',
        (22.37214699, 33.96614257): '奎宿_Legs_Wood',
        (33.96614257, 46.93116249): '婁宿_Bond_Metal',
        (46.93116249, 59.40804317): '胃宿_Stomach_Earth',
        (59.40804317, 68.46117549): '昴宿_Hairy_Head_Sun_element',
        (68.46117549, 83.70296314): '畢宿_Net_Moon_element',
        (83.70296314, 84.67745824): '觜宿_Turtle_Beak_Fire',
        (84.67745824, 95.29802279): '参宿_Three_Stars_Water',
        (95.29802279, 125.7245614): '井宿_Well_Wood',
        (125.7245614, 130.3004766): '鬼宿_Ghost_Metal',
        (130.3004766, 147.275341): '柳宿_Willow_Earth',
        (147.275341, 155.6873952): '星宿_Star_Sun_element',
        (155.6873952, 173.6855706): '張宿_Extended_Net_Moon_element',
        (173.6855706, 190.7217613): '翼宿_Wings_Fire',
	    (190.7217613, 203.8374893): '軫宿_Chariot_Water'
        }
            elements = {'Wood': ['角宿_Horn_Wood', '斗宿_Dipper_Wood', '奎宿_Legs_Wood', '井宿_Well_Wood'],
                'Metal': ['亢宿_Neck_Metal', '牛宿_Ox_Metal', '婁宿_Bond_Metal', '鬼宿_Ghost_Metal'],
                'Earth': ['氐宿_Root_Earth', '女宿_Girl_Earth', '胃宿_Stomach_Earth', '柳宿_Willow_Earth'],
                'Sun_element': ['房宿_Room_Sun_element', '虚宿_Emptiness_Sun_element', '昴宿_Hairy_Head_Sun_element', '星宿_Star_Sun_element'],
                'Moon_element': ['心宿_Heart_Moon_element', '危宿_Rooftop_Moon_element', '畢宿_Net_Moon_element', '張宿_Extended_Net_Moon_element'],
                'Fire': ['尾宿_Tail_Fire', '室宿0前_Encampment_Fire', '室宿0後_Encampment_Fire', '觜宿_Turtle_Beak_Fire', '翼宿_Wings_Fire'],
                'Water': ['箕宿_Winnowing_Basket_Water', '壁宿_Wail_Water', '参宿_Three_Stars_Water', '軫宿_Chariot_Water']}
    
            for (start, end), position in positions.items():
                if start <= ecl_lon and ecl_lon < end:
                    degree = ecl_lon - start
                    for element, mansions in elements.items():
                        if position in mansions:
                            return pd.Series([position, degree, element])
            return pd.Series(['Unknown', 0, 'Unknown'])


# Real 13 Astronomy Zodiac Boundaries
    def  real_astronomy_boundaries(ecl_lon): 
            astroboundaries ={
            (29.990947097601, 50.0584108063275): 'RealPsc_真雙魚',
            (50.0584108063275, 87.862732292416): 'RealAri_真白羊',
            (87.862732292416, 120.597871267582): 'RealTau_真金牛',
            (120.597871267582, 141.747390945472): 'RealGem_真雙子',
            (141.747390945472, 171.424861016967): 'RealCnc_真巨蟹',
            (171.424861016967, 222.620766163535): 'RealLeo_真獅子',
            (222.620766163535, 239.165751139665): 'RealVir_真處女',
            (239.165751139665, 246.093256694463): 'Real_真天秤',
            (246.093256694463, 267.299362072746): 'RealSco_真天蠍',
            (267.299362072746, 296.743047111097): 'RealOph_真蛇夫',
            (296.743047111097, 326.127854996387): 'RealSgr_真人馬',
            (326.127854996387, 350.013094049456): 'RealCap_真山羊',
            (350.013094049456, 359.9999999): 'RealAqr_真水瓶to360',
            (0.0, 29.990947097601): 'RealAqr_真水瓶from0'
            }
            for (start, end), astroboundary in astroboundaries.items():
                if start <= ecl_lon and ecl_lon < end:
                    degree = ecl_lon - start
                    return pd.Series([astroboundary, degree])

    all_data_df = pd.DataFrame(all_data)
    print(all_data_df.columns)


# Add solar terms, zodiac signs and zodiac degree to the DataFrame
# Acquire all the planet's Zodiac signs and degree, Mansion positions and degree, Astronomy boundaries and degree
# Zodiac signs and degree are Wetern Astrology‘s Whole House System, and Astronomy boundaries are the actual boundaries, I use midpoint of 2 stars to define the actual boundaries
planet_positions = {
        'Sun': 'Sun_ELONG',
        'Moon': 'Moon_ELONG',
        'Mars': 'Mars_ELONG',
        'Mercury': 'Mercury_ELONG',
        'Jupiter': 'Jupiter_ELONG',
        'Venus': 'Venus_ELONG',
        'Saturn': 'Saturn_ELONG',
        'Neptune': 'Neptune_ELONG',
        'Uranus': 'Uranus_ELONG',
        'Pluto': 'Pluto_ELONG',
        }


#24節氣
all_data_df[['Chinese_Sun_ELONG', 'Chinese_solar_terms', 'Chinese_lunar_month', 'Elements']] = all_data_df['Sun_ELONG'].apply(lambda x: pd.Series(solar_terms(x)))

# 將五行的“旺”、“相”，“休”，“囚”，“死”分成單獨的列
all_data_df['旺'] = all_data_df['Elements'].apply(lambda x: x[0])
all_data_df['相'] = all_data_df['Elements'].apply(lambda x: x[1])
all_data_df['休'] = all_data_df['Elements'].apply(lambda x: x[2])
all_data_df['囚'] = all_data_df['Elements'].apply(lambda x: x[3])
all_data_df['死'] = all_data_df['Elements'].apply(lambda x: x[4])

# 刪除Elements列，因為我們已經將其拆分為單獨的列
all_data_df.drop('Elements', axis=1, inplace=True)

# Define a list of all planets and points of interest
planets_and_points = [
    *planet_positions.keys(),
    'Moon_North_Node_ELONG',
    'Moon_South_Node_ELONG',
    'Lilith_ELONG',
    'Selena_ELONG',
    'ASC',
    'MC',
    'Year_Degree'
]

# Loop through the list and apply the zodiac_sign function
for item in planets_and_points:
    all_data_df[[f"{item}_Zodiac_signs", f"{item}_Zodiac_sign_element", f"{item}_Zodiac_degree"]] = all_data_df[item].apply(zodiac_sign)

# Calculate Life_sign and Life_sign_degree
all_data_df['Life_sign'] = all_data_df['ASC_Zodiac_signs']
all_data_df['Life_sign_degree'] = all_data_df['Sun_ELONG_Zodiac_degree']

# 定義一個函數，將黃道十二星座轉換為相對應的起始度數
def zodiac_sign_to_starting_degree(zodiac_sign):
    zodiac_degrees = {
        "Aries_Fire": 0,
        "Taurus_Metal": 30,
        "Gemini_Water": 60,
        "Cancer_Moon": 90,
        "Leo_Sun": 120,
        "Virgo_Water": 150,
        "Libra_Metal": 180,
        "Scorpio_Fire": 210,
        "Sagittarius_Wood": 240,
        "Capricorn_Earth": 270,
        "Aquarius_Earth": 300,
        "Pisces_Wood": 330
        }
    return zodiac_degrees[zodiac_sign]
  

# Calculate Life_degree
all_data_df['Life_degree'] = all_data_df['Life_sign'].apply(zodiac_sign_to_starting_degree) + all_data_df['Life_sign_degree']

# Calculate mansion_position for all planets and points of interest, including Life_degree
for item in planets_and_points + ['Life_degree']:
    all_data_df[[f"{item}_Mansion_positions", f"{item}_Mansion_degree", f"{item}_Mansion_element"]] = all_data_df[item].apply(mansion_position)

# Calculate real_astronomy_boundaries for all planets and points of interest, excluding Year_Degree
for item in planets_and_points[:-1]:
    all_data_df[[f"{item}_Astronomy_boundary", f"{item}_Astronomy_degree"]] = all_data_df[item].apply(real_astronomy_boundaries)

# Export the DataFrame to a CSV file
all_data_df.to_csv("/Users/jacky/Desktop/EXPORT_ALL_DATA_Y2006to2023.csv", index=False)
