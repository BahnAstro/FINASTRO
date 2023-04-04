from astroquery.simbad import Simbad
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, BarycentricTrueEcliptic
import pandas as pd

# Define a function to compute the midpoint between two coordinates
def compute_midpoint(coord1, coord2):
    pa = coord1.position_angle(coord2)
    sep = coord1.separation(coord2)
    midpoint = coord1.directional_offset_by(pa, sep/2)
    return midpoint

# Define the list of star names and their coordinates
star_names = ["99 Psc", "gam Ari", "41 Ari", "2 Tau", "zet Tau", "1 Gem", "kap Gem", "gam Cnc", "alf Cnc", "alf Leo", "sig Leo", "3 Vir", "107 Vir", "9 Lib", "38 Lib", "8 Sco", "14 Sco", "psi Oph", "tet Oph", "13 Sgr", "rho01 Sgr", "bet01 Cap", "del Cap", "iot Aqr", "phi Aqr", "kap Psc"]
star_coords = [SkyCoord.from_name(name) for name in star_names]

# Define the pairs of stars for which to compute midpoints

pairs = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15), (16, 17), (18, 19), (20, 21), (22, 23), (24, 25)]

# Import time, location and elevation(height) from excel file
data1 = pd.read_csv('/Users/x/Desktop/readdata/eqtest3.csv', names=['time', 'lat', 'lon', 'elevation'], skiprows=1, encoding='ISO-8859-1')

# Define a list to store the results
results = []

# Define the list of boundary names
boundary_names = ["PscAri_雙魚白羊界", "AriTau_白羊金牛界", "TauGem_金牛雙子界", "GemCnc_雙子巨蟹界", "CncLeo_巨蟹獅子界", "LeoVir_獅子處女界", "VirLib_處女天秤界", "LibSco_天秤天蠍界", "ScoOph_天蠍蛇夫界", "OphSgr_蛇夫人馬界", "SgrCap_人馬山羊界", "CapAgr_山羊水瓶界", "AqrPsc_水瓶雙魚界"]

# Run through all the data in excel
for index, row in data1.iterrows():
    # Define the observation time, location, and elevation
    observe_time_str = row['time']
    observe_time = Time(observe_time_str, scale='utc')
    observe_lat = row['lat'] * u.deg #you can input the latitude to replace row['lat'], e.g. London = 51.5 * u.deg
    observe_lon = row['lon'] * u.deg #you can input the longitude to replace row['lon'], e.g. London = -0.17 * u.deg
    observe_elevation = row['elevation'] * u.m #you can input the longitude to replace row['elevation'], e.g.  25 * u.m
    observe_location = EarthLocation(lat=observe_lat, lon=observe_lon, height=observe_elevation)

    # Compute the midpoints between each pair of stars
    for i, pair in enumerate(pairs):
        star1 = star_coords[pair[0]]
        star2 = star_coords[pair[1]]
        midpoint = compute_midpoint(star1, star2)
    
        # Convert the midpoint to ecliptic coordinates
        ecliptic_midpoint = midpoint.transform_to(BarycentricTrueEcliptic)
    
        results.append({'Boundary': boundary_names[i], 'Star 1': star_names[pair[0]], 'Star 2': star_names[pair[1]], 'Time': observe_time_str, 'Latitude': observe_lat.value, 'Longitude': observe_lon.value, 'Elevation': observe_elevation.value, 'RA': midpoint.ra.deg, 'Dec': midpoint.dec.deg, 'Ecliptic Longitude': ecliptic_midpoint.lon.deg, 'Ecliptic Latitude': ecliptic_midpoint.lat.deg})

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Group the results by time
grouped = df.groupby('Time')

# Create a list to store the dataframes for each time
dfs_by_time = []

# Iterate through the groups and create a dataframe for each time
for time, group in grouped:
    temp_df = group[['Boundary', 'Star 1', 'Star 2', 'RA', 'Dec', 'Ecliptic Longitude', 'Ecliptic Latitude']]
    temp_df = temp_df.rename(columns={'RA': f'RA ({time})', 'Dec': f'Dec ({time})', 'Ecliptic Longitude': f'Ecliptic Longitude ({time})', 'Ecliptic Latitude': f'Ecliptic Latitude ({time})'})
    temp_df = temp_df.set_index(['Boundary', 'Star 1', 'Star 2'])
    dfs_by_time.append(temp_df)

# Concatenate the dataframes for each time along the columns
final_df = pd.concat(dfs_by_time, axis=1)

# Export the final dataframe to a CSV file
final_df.to_csv('/Users/x/Desktop/real_zodiac_boundaries.csv')
