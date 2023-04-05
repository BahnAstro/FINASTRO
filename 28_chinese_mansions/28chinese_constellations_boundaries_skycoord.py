import pandas as pd
from astropy.coordinates import SkyCoord, BarycentricTrueEcliptic, EarthLocation
from astropy import units as u
from astropy.time import Time

# read CSV file to obtain 'time', 'lat', 'lon', 'elevation'
data1 = pd.read_csv('/Users/x/Desktop/eqtest3.csv', names=['time', 'lat', 'lon', 'elevation'], skiprows=1, encoding='ISO-8859-1')

mansion_boundaries = [
    "Spica", "kappa vir", "alpha1 lib", "pi scorpii", "Alpha Scorpii", "mu1 scorpii", "Gamma2 Sagittarii", "phi Sagittarii",
    "beta Capricorni", "Epsilon Aquarii", "beta Aquarii", "alpha Aquarii", "Alpha Pegasi", "gamma Pegasi", "eta Andromedae",
    "beta Arietis", "35 Arietis", "17 Tauri", "epsilon Tauri", "lambda Orionis", "zet Ori A", "HR 2286", "Theta Cancri",
    "delta Hydrae", "Alphard", "upsilon1 Hydrae", "alpha Crateris", "gamma Corvi"
]

mansion_boundaries_coords = [SkyCoord.from_name(name) for name in mansion_boundaries]

def get_ecliptic_coordinates(ra, dec):
    sky_coord = SkyCoord(ra, dec, frame='icrs', unit=(u.hourangle, u.deg))
    return sky_coord.transform_to(BarycentricTrueEcliptic)

ecliptic_coords = []
radec_coords = []

for index, row in data1.iterrows():
    observe_time_str = row['time']
    observe_time = Time(observe_time_str, scale='utc')
    observe_lat = row['lat'] * u.deg
    observe_lon = row['lon'] * u.deg
    observe_elevation = row['elevation'] * u.m
    observe_location = EarthLocation(lat=observe_lat, lon=observe_lon, height=observe_elevation)

    time_ecliptic_coords = []
    time_radec_coords = []

    for coord in mansion_boundaries_coords:
        ecl_coord = get_ecliptic_coordinates(coord.ra, coord.dec)
        time_ecliptic_coords.extend([ecl_coord.lon.deg, ecl_coord.lat.deg]) 
        time_radec_coords.extend([coord.ra.deg, coord.dec.deg])  

    ecliptic_coords.append(time_ecliptic_coords)
    radec_coords.append(time_radec_coords)

columns_ecl = [f"{name}_lon_deg" for name in mansion_boundaries] + [f"{name}_lat_deg" for name in mansion_boundaries]
columns_radec = [f"{name}_ra_deg" for name in mansion_boundaries] + [f"{name}_dec_deg" for name in mansion_boundaries]

output_data_ecl = pd.DataFrame(ecliptic_coords, columns=columns_ecl)
output_data_radec = pd.DataFrame(radec_coords, columns=columns_radec)

output_data = pd.concat([data1['time'], output_data_radec, output_data_ecl], axis=1)  # 将时间、RA、Dec 和黄经、黄纬数据合并

output_data.to_csv('/Users/jacky/x/28mansions_result.csv', index=False)
