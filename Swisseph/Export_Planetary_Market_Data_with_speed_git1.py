import swisseph as swe
import math
from datetime import datetime
import pytz
import numpy as np
import csv
import pandas as pd
import math

readdata1 = pd.read_csv("/Users/x/daily_high_low_2006_v3_1.csv", header=None, skiprows=1, names=['DateTime', 'Open', 'High', 'Low', 'Close', 'HL'], encoding='ISO-8859-1')


# Convert time column to pandas datetime object
time_pd = pd.to_datetime(readdata1['DateTime'], format='%Y-%m-%d %H:%M:%S')


# Set GeoLat, GeoLon
latitude = 22.283875
longitude = 114.158229



# 循環處理每個從CSV輸入的時間
all_data = []
for idx, row in readdata1.iterrows():

    time_pd = row["DateTime"]
    # 将日期字符串转换为 pandas.Timestamp 对象，并将其转换为 UTC 时间
    utc_date = pd.to_datetime(time_pd)
    #计算儒略日
    jd = swe.julday(utc_date.year, utc_date.month, utc_date.day, utc_date.hour + utc_date.minute / 60.0 + utc_date.second / 3600.0)

    def calc_asc_mc(latitude, longitude, utc_date):
        cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
        ascendant = ascmc[0]
        midheaven = ascmc[1]
        descendant = cusps[6]
        imum_coeli = cusps[3]
        equ_ascendant = ascmc[4]

        return ascendant, midheaven, descendant, imum_coeli, equ_ascendant
    
    ascendant, midheaven, descendant, imum_coeli, equ_ascendant = calc_asc_mc(latitude, longitude, utc_date)

    single_row_data = {
        'Time': utc_date,
        'Open': row['Open'],
        'High': row['High'],
        'Low': row['Low'],
        'Close': row['Close'],
        'HL': row['HL'],
        'ASC':ascendant,
        'MC':midheaven,
        'DES': descendant,
        'IC': imum_coeli,
        'EQU_ASC' : equ_ascendant

        }


        #ascendant, midheaven, descendant, imum_coeli = calc_asc_mc(latitude, longitude, utc_date)
   
    # 計算天體位置
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
        "PLUTO": swe.PLUTO
    }

    speed_thresholds = {
    "STATIONARY": 0.1,
    "SLOW": 0.5,
    "FAST": 1.5,
    }


#Solar and Lunar Eclipse
#    def is_eclipse(jd, name, planet):
 #       if planets == "Sun":
#            eclipse_type, _ = swe.sol_eclipse_when_glob(jd, swe.FLG_SWIEPH)
 #           if eclipse_type != 0:
 #               return True
 #       elif planets == "Moon":
 #           lun_eclipse, _ = swe.lun_eclipse_when(jd, swe.FLG_SWIEPH)
 #           if lun_eclipse != 0:
 #               return True
 #       return False

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
    
    # 設定計算標誌
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
 
    
        #print(f"{name}_ELONG:", elong)
        #print(f"{name}_ELAT:", elat)
        #print(f"{name}_RA:", ra)
        #print(f"{name}_DEC:", dec)

    # Part of Fortune 幸運點
    #def calculate_fortune(asc, sun_long, moon_long, utc_date, latitude, longitude):
    
     #   rise_flags = swe.CALC_RISE | swe.CALC_SET | swe.FLG_SWIEPH
     #   rise_time, is_rising = swe.rise_trans(jd, swe.SUN, None, swe.CALC_RISE, (longitude, latitude, 0))
     #   set_time, is_setting = swe.rise_trans(jd, swe.SUN, None, swe.CALC_SET, (longitude, latitude, 0))

    
     #   rise_time_utc = swe.jdut1_to_utc(rise_time[1], swe.GREG_CAL)
     #   set_time_utc = swe.jdut1_to_utc(set_time[1], swe.GREG_CAL)
    
     #   daytime = rise_time_utc < utc_date < set_time_utc
     #   if daytime:
     #       sun_moon_angle = moon_long - sun_long
     #   else:
     #       sun_moon_angle = sun_long - moon_long
        
      #  fortune_long = asc + sun_moon_angle
      #  fortune_long %= 360
    
      #  return fortune_long
    #def calculate_fortune(ascendant, sun_long, moon_long, utc_date, latitude, longitude):
    #    jd = swe.utc_to_jd(utc_date.year, utc_date.month, utc_date.day, utc_date.hour, utc_date.minute, utc_date.second, swe.GREG_CAL)[1]

    # Calculate sunrise and sunset times using swe_rise_trans
    #    rise_flags = swe.CALC_RISE | swe.BIT_DISC_CENTER
    #    set_flags = swe.CALC_SET | swe.BIT_DISC_CENTER

    #    _, jd_sunrise = swe.rise_trans(jd, swe.SUN, "", rise_flags, (longitude, latitude, 0))
    #    _, jd_sunset = swe.rise_trans(jd, swe.SUN, "", set_flags, (longitude, latitude, 0))

    # Check if the current time is between sunrise and sunset
    #    is_daytime = jd_sunrise < jd < jd_sunset

    # Calculate fortune point based on daytime or nighttime
    #    if is_daytime:
    #        fortune_long = ascendant + moon_long - sun_long
    #    else:
    #        fortune_long = ascendant + sun_long - moon_long

     #   fortune_long = fortune_long % 360
     #   return fortune_long

    # 在 for idx, row in readdata1.iterrows(): 循环内部添加以下代码
    #fortune_long = calculate_fortune(ascendant, single_row_data["Sun_ELONG"], single_row_data["Moon_ELONG"], utc_date, latitude, longitude)
    #single_row_data.update({"Fortune_Longitude": fortune_long})




    # 计算月球北交点、南交点和莉莉丝

    moon_nodes, ret = swe.calc_ut(jd, swe.MEAN_NODE)
    mean_lilith, ret = swe.calc_ut(jd, swe.MEAN_APOG)
    mean_lilith_lon = mean_lilith[0]
    mean_lilith_lat = mean_lilith[1]
    mean_lilith_dist = mean_lilith[2]

    moon_true_node, ret, = swe.calc_ut(jd, swe.TRUE_NODE)
    true_node = moon_true_node [1]

    moon_north_node_lon = moon_nodes[0]
    #moon_north_node_lat = moon_nodes[1]
    moon_south_node_lon = (moon_nodes[0] + 180) % 360
    #moon_south_node_lat = -moon_nodes[1]
    # Selena的基礎年份
    purple_period = 10227.1792
    purple_base_date = pd.Timestamp('1975-03-13 16:00:00', tz='UTC')
    purple_base_degree = 230.5

    # 定義Selena周期
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
        #selena_lat = 0  # 假设 Selena 在黄道平面上

        #selena_ra, selena_dec = ecl2equ(jd, selena_long, selena_lat)

     
    single_row_data.update({
        "Moon_North_Node_LON": moon_north_node_lon,
        "Moon_South_Node_LON": moon_south_node_lon,
        "Lilith_LON": mean_lilith_lon,
        "Lilith_LAT": mean_lilith_lat,
        "Lilith_DIST": mean_lilith_dist,
        "Selena_LONG": selena_long
        })
 

#Extra Data for South Node and North node
#"Moon_North_Node_RA": moon_north_node_ra,
#"Moon_South_Node_RA": moon_south_node_ra,
#"Lilith_RA": mean_lilith_ra,



    
        #            "Selena_RA": selena_ra,
        #    "Selena_DEC": selena_dec
        #print(f"Purple Position: {purple_position}")
    
    #def ecl2equ(jd, lon, lat):
    #    ecl_obl = swe.calc_eps(jd)[0]
    #    x = math.cos(math.radians(lon)) * math.cos(math.radians(lat))
    #    y = math.sin(math.radians(lon)) * math.cos(math.radians(lat)) * math.cos(math.radians(ecl_obl)) - math.sin(math.radians(lat)) * math.sin(math.radians(ecl_obl))
    #    z = math.sin(math.radians(lon)) * math.cos(math.radians(lat)) * math.sin(math.radians(ecl_obl)) + math.sin(math.radians(lat)) * math.cos(math.radians(ecl_obl))

    #    ra = math.degrees(math.atan2(y, x))
    #    dec = math.degrees(math.atan2(z, math.sqrt(x * x + y * y)))

    #    if ra < 0:
    #        ra += 360

    #    return ra, dec

    #moon_north_node_ra, moon_north_node_dec = ecl2equ(jd, moon_north_node_lon, 0)
    #moon_south_node_ra, moon_south_node_dec = ecl2equ(jd, moon_south_node_lon, 0)
    #mean_lilith_ra, mean_lilith_dec = ecl2equ(jd, mean_lilith_lon, mean_lilith_lat)




    all_data.append(single_row_data)
#print(all_data)
export_all_data = pd.DataFrame(all_data)
export_all_data.to_csv("/Users/x/Desktop/PLANET_ALLDATA_ERA1.csv", index=False)


