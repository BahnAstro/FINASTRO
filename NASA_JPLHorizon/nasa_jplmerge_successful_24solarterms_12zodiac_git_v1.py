from astroquery.jplhorizons import Horizons
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord, EarthLocation, BarycentricTrueEcliptic
import swisseph as swe
from datetime import datetime
from astropy.time import Time
import numpy as np
import pandas as pd
import csv
import pytz



# Read data from CSV file
data_original = pd.read_csv("/Users/x/daily_high_low_2006.csv", header=None, skiprows=1, names=['DateTime', 'Open', 'High', 'Low', 'Close', 'HL'], encoding='ISO-8859-1')

# Convert time column to pandas datetime object
time_pd = pd.to_datetime(data_original['DateTime'], format='%Y-%m-%d %H:%M:%S')

# Convert pandas datetime object to string format
time_str = time_pd.dt.strftime('%Y-%m-%d %H:%M:%S')

# Replace time column in data with string format
data_original['DateTime'] = time_str

# Create an empty DataFrame to store the data for all times
data_all = pd.DataFrame()

# Add original data columns to data_all
data_all[['Open', 'High', 'Low', 'Close', 'HL']] = data_original.loc[:, ['Open', 'High', 'Low', 'Close', 'HL']]


# Set Observer Location on Earth
observer_location = {'lon': 114.158229, 'lat': 22.283875, 'elevation': 0}

# Set Target Planets
target_list = ['10', '301', '4', '199', '5', '299', '6', '7', '8', '9']
target_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Neptune', 'Uranus', 'Pluto']

# Create an empty DataFrame to store the data for all times
data_all = pd.DataFrame()

data_all['Sun_solar_term'] = None
data_all['Zodiac_signs'] = None
data_all['Zodiac_degree'] = None
data_all['Mansion_positions'] = None
data_all['Mansion_degree'] = None
data_all['Astronomy_boundary'] = None
data_all['Astronomy_degree'] = None

# Drop duplicate rows based on the 'DateTime' column
data_original = data_original.drop_duplicates(subset='DateTime', keep='first')

# Create a dictionary from the data_original DataFrame with 'DateTime' as the key
original_data_dict = data_original.set_index('DateTime').to_dict(orient='index')

# Loop over start times
#for start_time in data_original['DateTime']:
for idx, row in data_original.iterrows():
    # Convert start_time to astropy Time object

    time_pd = row["DateTime"]
    # 将日期字符串转换为 pandas.Timestamp 对象，并将其转换为 UTC 时间
    #utc_date = pd.to_datetime(time_pd)

    #start_time=utc_date
    t = Time(time_pd, format='iso', scale='utc')

    # Create an empty DataFrame to store the data for this time
    data = pd.DataFrame(columns=['RA', 'DEC', 'ObsEclLon', 'ObsEclLat', 'illumination', 'AZ', 'EL', 'target'])

    # Use Loops to acquire targets' DATA
    for target, name in zip(target_list, target_names):
        obj = Horizons(id=target, location=observer_location, epochs=t.jd)
        eph = obj.ephemerides()

        # Convert the table to a pandas DataFrame and filter to include only the required columns
        planetdata = eph.to_pandas()[['datetime_str', 'datetime_jd', 'RA', 'DEC', 'ObsEclLon', 'ObsEclLat', 'illumination', 'AZ', 'EL']]

        # Add the target ID and name to the DataFrame
        planetdata['target'] = name

        # Append the data to the main DataFrame
        data = pd.concat([data, planetdata], ignore_index=True)
    
        # Pivot the DataFrame to have the data for each target in a separate column range
        data_pivot = data.pivot(index='datetime_str', columns='target', values=['RA', 'DEC', 'ObsEclLon', 'ObsEclLat', 'illumination', 'AZ', 'EL'])


    def solar_terms(ecl_lon):
            terms = [
        (315, 330, 'Beginning_of_Spring_立春'),
        (330, 345, 'First_month_midpoint_雨水'),
        (345, 0, 'Second_month_midpoint_驚蟄'),
        (0, 15, 'Spring_Equinox_春分'),
        (15, 30, 'First_april_清明'),
        (30, 45, 'Second_april_穀雨'),
        (45, 60, 'Beginning_of_Summer_立夏'),
        (60, 75, 'First_month_midpoint_小滿'),
        (75, 90, 'Second_month_midpoint_芒種'),
        (90, 105, 'Summer_Solstice_夏至'),
        (105, 120, 'First_july_小暑'),
        (120, 135, 'Second_july_大暑'),
        (135, 150, 'Beginning_of_Autumn_立秋'),
        (150, 165, 'First_month_midpoint_處暑'),
        (165, 180, 'Second_month_midpoint_白露'),
        (180, 195, 'Autumn_Equinox_秋分'),
        (195, 210, 'First_october_寒露'),
        (210, 225, 'Second_october_霜降'),
        (225, 240, 'Beginning_of_Winter_立冬'),
        (240, 255, 'First_month_midpoint_小雪'),
        (255, 270, 'Second_month_midpoint_大雪'),
        (270, 285, 'Winter_Solstice_冬至'),
        (285, 300, 'First_january_小寒'),
        (300, 315, 'Second_january_大寒'),
        ]

            for start, end, term in terms:
                if start > end:
                    if ecl_lon >= start or ecl_lon < end:
                        return term
                else:
                    if ecl_lon >= start and ecl_lon < end:
                        return term
            return None
    
    def zodiac_sign(ecl_lon):
            signs = {
        (0, 30): 'Aries',
        (30, 60): 'Taurus',
        (60, 90): 'Gemini',
        (90, 120): 'Cancer',
        (120, 150): 'Leo',
        (150, 180): 'Virgo',
        (180, 210): 'Libra',
        (210, 240): 'Scorpio',
        (240, 270): 'Sagittarius',
        (270, 300): 'Capricorn',
        (300, 330): 'Aquarius',
        (330, 360): 'Pisces'
        }
            for (start, end), sign in signs.items():
                if start <= ecl_lon < end:
                    degree = ecl_lon - start
                    return pd.Series([sign, degree])
            return None
    
    def mansion_position(ecl_lon):
            positions = {
        (203.8374893, 214.4898543): '角宿',
        (214.4898543, 225.0215638): '亢宿',
        (225.0215638, 242.9360091): '氐宿',
        (242.9360091, 249.7584245): '房宿',
        (249.7584245, 256.1517382): '心宿',
        (256.1517382, 271.2575671): '尾宿',
        (271.2575671, 280.1774751): '箕宿',
        (280.1774751, 304.0435179): '斗宿',
        (304.0435179, 311.7193257): '牛宿',
        (311.7193257, 323.3911983): '女宿',
        (323.3911983, 333.348599): '虚宿',
        (333.348599, 353.481734): '危宿',
        (353.481734, 360): '室宿0前',
        (0, 9.152166707): '室宿0後',
        (9.152166707, 22.37214699): '壁宿',
        (22.37214699, 33.96614257): '奎宿',
        (33.96614257, 46.93116249): '婁宿',
        (46.93116249, 59.40804317): '胃宿',
        (59.40804317, 68.46117549): '昴宿',
        (68.46117549, 83.70296314): '畢宿',
        (83.70296314, 84.67745824): '觜宿',
        (84.67745824, 95.29802279): '参宿',
        (95.29802279, 125.7245614): '井宿',
        (125.7245614, 130.3004766): '鬼宿',
        (130.3004766, 147.275341): '柳宿',
        (147.275341, 155.6873952): '星宿',
        (155.6873952, 173.6855706): '張宿',
        (173.6855706, 190.7217613): '翼宿',
	    (190.7217613, 203.8374893): '軫宿'
        }
            for (start, end), position in positions.items():
                if start <= ecl_lon < end:
                    degree = ecl_lon - start
                    return pd.Series([position, degree])
        # Return a default value when input is outside of the defined ranges
            return pd.Series(['Unknown', 0])

    def  real_astronomy_boundaries(ecl_lon): 
            astroboundaries ={
            (29.990947097601, 50.0584108063275): 'PscAri_雙魚白羊界',
            (50.0584108063275, 87.862732292416): 'AriTau_白羊金牛界',
            (87.862732292416, 120.597871267582): 'TauGem_金牛雙子界',
            (120.597871267582, 141.747390945472): 'GemCnc_雙子巨蟹界',
            (141.747390945472, 171.424861016967): 'CncLeo_巨蟹獅子界',
            (171.424861016967, 222.620766163535): 'LeoVir_獅子處女界',
            (222.620766163535, 239.165751139665): 'VirLib_處女天秤界',
            (239.165751139665, 246.093256694463): 'LibSco_天秤天蠍界',
            (246.093256694463, 267.299362072746): 'ScoOph_天蠍蛇夫界',
            (267.299362072746, 296.743047111097): 'OphSgr_蛇夫人馬界',
            (296.743047111097, 326.127854996387): 'SgrCap_人馬山羊界',
            (326.127854996387, 350.013094049456): 'CapAgr_山羊水瓶界',
            (350.013094049456, 360): 'AqrPsc_水瓶雙魚界to 360',
            (0.0, 29.990947097601): 'AqrPsc_水瓶雙魚界from 0'
            }
            for (start, end), astroboundary in astroboundaries.items():
                if start <= ecl_lon < end:
                    degree = ecl_lon - start
                    return pd.Series([astroboundary, degree])
                
        # Return a default value when input is outside of the defined ranges
            return pd.Series(['Unknown', 0])
       

    # Flatten the column names of the pivoted DataFrame and reorder them according to the target_names list
    data_pivot.columns = [f"{col[1]}_{col[0]}" for col in data_pivot.columns.to_flat_index()]
    data_pivot = data_pivot.reindex(columns=[f"{name}_{col}" for col in ['RA', 'DEC', 'ObsEclLon', 'ObsEclLat', 'illumination', 'AZ', 'EL'] for name in target_names])

    # Add the time columns to the DataFrame
    data_pivot['datetime_str'] = time_pd
    data_pivot['datetime_jd'] = t.jd   
    data_pivot[['Open', 'High', 'Low', 'Close', 'HL']] = pd.Series(original_data_dict[time_pd])

    # Add the data to the main DataFrame
    data_all = pd.concat([data_all, data_pivot], ignore_index=True)
    
# Add solar terms, zodiac signs and zodiac degree to the DataFrame
data_all['Sun_solar_term'] = data_all['Sun_ObsEclLon'].apply(solar_terms)

# Acquire all the planet's Zodiac signs and degree, Mansion positions and degree, Astronomy boundaries and degree
# Zodiac signs and degree are Wetern Astrology‘s Whole House System, and Astronomy boundaries are the actual boundaries, I use midpoint of 2 stars to define the actual boundaries
planet_positions = {
    'Sun': 'Sun_ObsEclLon',
    'Moon': 'Moon_ObsEclLon',
    'Mars': 'Mars_ObsEclLon',
    'Mercury': 'Mercury_ObsEclLon',
    'Jupiter': 'Jupiter_ObsEclLon',
    'Venus': 'Venus_ObsEclLon',
    'Saturn': 'Saturn_ObsEclLon',
    'Neptune': 'Neptune_ObsEclLon',
    'Uranus': 'Uranus_ObsEclLon',
    'Pluto': 'Pluto_ObsEclLon'
    }

# 獲取行星黃經所在的星座和星座度數
for planet, pos in planet_positions.items():
    data_all[[f"{planet}_Zodiac_signs", f"{planet}_Zodiac_degree"]] = data_all[pos].apply(zodiac_sign).apply(pd.Series)
    
# 獲取行星所在的宮位和度數
for planet, pos in planet_positions.items():
    data_all[[f"{planet}_Mansion_positions", f"{planet}_Mansion_degree"]] = data_all[pos].apply(mansion_position)
    
# 獲取行星所在的區域和度數
for planet, pos in planet_positions.items():
    data_all[[f"{planet}_Astronomy_boundary", f"{planet}_Astronomy_degree"]] = data_all[pos].apply(real_astronomy_boundaries)

# Create an empty DataFrame to store the moon orbital elements data
moon_data_all = pd.DataFrame()

# Loop over start times for Moon orbital elements
for time_pd in data_all['datetime_str']:
    # Convert start_time to astropy Time object
    t = Time(time_pd, format='iso', scale='utc')

    moon_target_list = ['301']
    moon_target_name = ['Moon']
    dataframes = []

    for moon_target, name in zip(moon_target_list, moon_target_name):
        obj = Horizons(id=moon_target, location='399', epochs=t.jd)
        eph = obj.elements()
        moon_data = eph.to_pandas()  # Convert astropy Table to pandas DataFrame
        dataframes.append(moon_data)

    # Add the time columns to the DataFrame
    moon_data['datetime_str'] = time_pd
    moon_data['datetime_jd'] = t.jd

    # Concatenate the DataFrames
    moon_data_all = pd.concat([moon_data_all, moon_data], ignore_index=True)


# Merge data_all and moon_data_all on the 'datetime_str' and 'datetime_jd' columns
merged_data = pd.merge(data_all, moon_data_all, on=['datetime_str', 'datetime_jd'])

# Get all column names except 'datetime_str' and 'datetime_jd'
column_names = [col for col in merged_data.columns if col not in ['datetime_str', 'datetime_jd', 'Open', 'High', 'Low', 'Close']]


# Add 'datetime_str', 'datetime_jd', 'Open', 'High', 'Low', 'Close' to the beginning of the column list
column_names = ['datetime_str', 'datetime_jd'] + [col for col in data_original.columns if col != 'DateTime'] + column_names

# Reorder the columns of the DataFrame
merged_data = merged_data[column_names]

# Save the merged DataFrame to a CSV file
merged_data.to_csv('/Users/x/Desktop/nasa_planetdata_astronomy_hk_BOSS1.csv', index=False)