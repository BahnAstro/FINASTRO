from astroquery.jplhorizons import Horizons
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord, EarthLocation, BarycentricTrueEcliptic
from datetime import datetime
from astropy.time import Time
import numpy as np
import pandas as pd

# Read data from CSV file
data = pd.read_csv('/Users/x/Desktop/eqtest3.csv', names=['time', 'lat', 'lon', 'elevation'], skiprows=1, encoding='ISO-8859-1')

# Convert time column to pandas datetime object
time_pd = pd.to_datetime(data['time'], format='%Y-%m-%d %H:%M:%S')
print(time_pd)

# Convert pandas datetime object to string format
time_str = time_pd.dt.strftime('%Y-%m-%d %H:%M:%S')

# Replace time column in data with string format
data['time'] = time_str

# Set Observer Location on Earth
observer_location = {'lon': data['lon'][0], 'lat': data['lat'][0], 'elevation': data['elevation'][0]}

# Set Target Planets
target_list = ['10', '301', '4', '199', '5', '299', '6', '7', '8', '9']
target_names = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Neptune', 'Uranus', 'Pluto']

# Create an empty DataFrame to store the data for all times
data_all = pd.DataFrame()

data_all['Sun_solar_term'] = None
data_all['Zodiac_signs'] = None
data_all['Zodiac_degree'] = None

# Loop over start times
for start_time in data['time']:
    # Convert start_time to astropy Time object
    t = Time(start_time, format='iso', scale='utc')

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
        for start, end in signs.keys():
            if start <= ecl_lon < end:
                return signs[(start, end)]
        return None

    def zodiac_degree(ecl_lon):
        return ecl_lon - int(ecl_lon / 30) * 30
        
        for start, end in signs.keys():
            if start <= ecl_lon < end:
                degree = ecl_lon - start
                return f"{signs[(start, end)]}_{degree:.7f}"
        return None
    
    # Flatten the column names of the pivoted DataFrame and reorder them according to the target_names list
    data_pivot.columns = [f"{col[1]}_{col[0]}" for col in data_pivot.columns.to_flat_index()]
    data_pivot = data_pivot.reindex(columns=[f"{name}_{col}" for col in ['RA', 'DEC', 'ObsEclLon', 'ObsEclLat', 'illumination', 'AZ', 'EL'] for name in target_names])

    # Add the time columns to the DataFrame
    data_pivot['datetime_str'] = start_time
    data_pivot['datetime_jd'] = t.jd   

    # Add the data to the main DataFrame
    data_all = pd.concat([data_all, data_pivot], ignore_index=True)
    


# Add solar terms, zodiac signs and zodiac degree to the DataFrame
data_all['Sun_solar_term'] = data_all['Sun_ObsEclLon'].apply(solar_terms)
data_all['Zodiac_signs'] = data_all['Sun_ObsEclLon'].apply(zodiac_sign)
data_all['Zodiac_degree'] = data_all['Sun_ObsEclLon'].apply(zodiac_degree)

# Create an empty DataFrame to store the moon orbital elements data
moon_data_all = pd.DataFrame()

# Loop over start times for Moon orbital elements
for start_time in data_all['datetime_str']:
    # Convert start_time to astropy Time object
    t = Time(start_time, format='iso', scale='utc')

    moon_target_list = ['301']
    moon_target_name = ['Moon']
    dataframes = []

    for moon_target, name in zip(moon_target_list, moon_target_name):
        obj = Horizons(id=moon_target, location='399', epochs=t.jd)
        eph = obj.elements()
        moon_data = eph.to_pandas()  # Convert astropy Table to pandas DataFrame
        dataframes.append(moon_data)

    # Add the time columns to the DataFrame
    moon_data['datetime_str'] = start_time
    moon_data['datetime_jd'] = t.jd

    # Concatenate the DataFrames
    moon_data_all = pd.concat([moon_data_all, moon_data], ignore_index=True)

# Merge data_all and moon_data_all on the 'datetime_str' and 'datetime_jd' columns
merged_data = pd.merge(data_all, moon_data_all, on=['datetime_str', 'datetime_jd'])

# Get all column names except 'datetime_str' and 'datetime_jd'
column_names = [col for col in merged_data.columns if col not in ['datetime_str', 'datetime_jd']]

# Add 'datetime_str' and 'datetime_jd' to the beginning of the column list
column_names = ['datetime_str', 'datetime_jd'] + column_names

# Reorder the columns of the DataFrame
merged_data = merged_data[column_names]

# Save the merged DataFrame to a CSV file
merged_data.to_csv('/Users/x/Desktop/nasa_planetdata_with_zodiacsign_solarterms.csv', index=False)
