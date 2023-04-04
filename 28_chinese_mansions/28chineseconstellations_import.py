from astroquery.simbad import Simbad
from astropy import units as u
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation
import pandas as pd
from datetime import datetime


# 查詢多個星體資訊

result_table = Simbad.query_objects(["Spica", "kappa vir", "alpha1 lib", "pi scorpii",  "Alpha Scorpii", "mu1 scorpii", "Gamma2 Sagittarii","phi Sagittarii", "beta Capricorni", "Epsilon Aquarii", "beta Aquarii", "alpha Aquarii", "Alpha Pegasi", "gamma Pegasi", "eta Andromedae", "beta Arietis", "35 Arietis", "17 Tauri", "epsilon Tauri", "lambda Orionis", "zet Ori A", "HR 2286", "Theta Cancri", "delta Hydrae", "Alphard", "upsilon1 Hydrae", "alpha Crateris", "gamma Corvi"])

# 獲取多個星體的坐標
for row in result_table:
    star_name = row['MAIN_ID']
    star_coord = SkyCoord(ra=row['RA'], dec=row['DEC'], unit=(u.hourangle, u.deg), frame='icrs')

#coords = [SkyCoord(ra=row['RA'], dec=row['DEC'], unit=(u.hourangle, u.deg), frame='icrs') for row in result_table]

spica_coord = SkyCoord(ra=result_table['RA'][0], dec=result_table['DEC'][0], unit=(u.hourangle, u.deg), frame='icrs')
kappa_vir_coord = SkyCoord(ra=result_table['RA'][1], dec=result_table['DEC'][1], unit=(u.hourangle, u.deg), frame='icrs')
alpha1_lib_coord = SkyCoord(ra=result_table['RA'][2], dec=result_table['DEC'][2], unit=(u.hourangle, u.deg), frame='icrs')
pi_scorpii_coord = SkyCoord(ra=result_table['RA'][3], dec=result_table['DEC'][3], unit=(u.hourangle, u.deg), frame='icrs')
alpha_Scorpii_coord = SkyCoord(ra=result_table['RA'][4], dec=result_table['DEC'][4], unit=(u.hourangle, u.deg), frame='icrs')
mu1_scorpii_coord =SkyCoord(ra=result_table['RA'][5], dec=result_table['DEC'][5], unit=(u.hourangle, u.deg), frame='icrs')
gamma2_sagittarii_coord =SkyCoord(ra=result_table['RA'][6], dec=result_table['DEC'][6], unit=(u.hourangle, u.deg), frame='icrs')
phi_sagittarii_coord =SkyCoord(ra=result_table['RA'][7], dec=result_table['DEC'][7], unit=(u.hourangle, u.deg), frame='icrs')
beta_capricorni_coord =SkyCoord(ra=result_table['RA'][8], dec=result_table['DEC'][8], unit=(u.hourangle, u.deg), frame='icrs')
epsilon_aquarii_coord =SkyCoord(ra=result_table['RA'][9], dec=result_table['DEC'][9], unit=(u.hourangle, u.deg), frame='icrs')
beta_aquarii_coord =SkyCoord(ra=result_table['RA'][10], dec=result_table['DEC'][10], unit=(u.hourangle, u.deg), frame='icrs')
alpha_Aquarii_coord=SkyCoord(ra=result_table['RA'][11], dec=result_table['DEC'][11], unit=(u.hourangle, u.deg), frame='icrs')
alpha_pegasi_coord=SkyCoord(ra=result_table['RA'][12], dec=result_table['DEC'][12], unit=(u.hourangle, u.deg), frame='icrs')
gamma_pegasi_coord=SkyCoord(ra=result_table['RA'][13], dec=result_table['DEC'][13], unit=(u.hourangle, u.deg), frame='icrs')
eta_andromedae_coord=SkyCoord(ra=result_table['RA'][14], dec=result_table['DEC'][14], unit=(u.hourangle, u.deg), frame='icrs')
beta_arietis_coord=SkyCoord(ra=result_table['RA'][15], dec=result_table['DEC'][15], unit=(u.hourangle, u.deg), frame='icrs')
arietis35_coord=SkyCoord(ra=result_table['RA'][16], dec=result_table['DEC'][16], unit=(u.hourangle, u.deg), frame='icrs')
tauri17_coord=SkyCoord(ra=result_table['RA'][17], dec=result_table['DEC'][17], unit=(u.hourangle, u.deg), frame='icrs')
epsilon_tauri_coord=SkyCoord(ra=result_table['RA'][18], dec=result_table['DEC'][18], unit=(u.hourangle, u.deg), frame='icrs')
lambda_orionis_coord=SkyCoord(ra=result_table['RA'][19], dec=result_table['DEC'][19], unit=(u.hourangle, u.deg), frame='icrs')
zet_Ori_A_coord=SkyCoord(ra=result_table['RA'][20], dec=result_table['DEC'][20], unit=(u.hourangle, u.deg), frame='icrs')
mu_gem_coord=SkyCoord(ra=result_table['RA'][21], dec=result_table['DEC'][21], unit=(u.hourangle, u.deg), frame='icrs')
theta_cancri_coord=SkyCoord(ra=result_table['RA'][22], dec=result_table['DEC'][22], unit=(u.hourangle, u.deg), frame='icrs')
delta_hydrae_coord=SkyCoord(ra=result_table['RA'][23], dec=result_table['DEC'][23], unit=(u.hourangle, u.deg), frame='icrs')
alphard_coord=SkyCoord(ra=result_table['RA'][24], dec=result_table['DEC'][24], unit=(u.hourangle, u.deg), frame='icrs')
upsilon1_hydrae_coord=SkyCoord(ra=result_table['RA'][25], dec=result_table['DEC'][25], unit=(u.hourangle, u.deg), frame='icrs')
alpha_crateris_coord=SkyCoord(ra=result_table['RA'][26], dec=result_table['DEC'][26], unit=(u.hourangle, u.deg), frame='icrs')
gamma_corvi_coord=SkyCoord(ra=result_table['RA'][27], dec=result_table['DEC'][27], unit=(u.hourangle, u.deg), frame='icrs')



# 从CSV文件导入特定时间、位置和海拔
data1 = pd.read_csv('/Users/x/Desktop/eqtest3.csv', names=['time', 'lat', 'lon', 'elevation'], skiprows=1, encoding='ISO-8859-1')

# 使用导入的数据定义特定时间和位置
observe_time_str = data1['time'][0]  # 获取CSV文件中的第一个时间数据
observe_time = Time(observe_time_str, scale='utc')
observe_lat = data1['lat'][0] * u.deg
observe_lon = data1['lon'][0] * u.deg
observe_elevation = data1['elevation'][0] * u.m

observe_location = EarthLocation(lat=observe_lat, lon=observe_lon, height=observe_elevation)

#====
# 計算每個星體在特定時間和位置的赤道位置
#star_equatorial = star_coord('fk5', time=observe_time, location=observe_location)

# 輸出多個星體在特定時間和位置的赤道位置
print(f"角宿一在 {observe_time}的赤經為{spica_coord.ra}, 赤緯為{spica_coord.dec}。")

#print(f"角宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{spica_coord.ra}, 赤緯為{spica_coord.dec}。")
#print(f"亢宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{kappa_vir_coord.ra}, 赤緯為{kappa_vir_coord.dec}。")
#print(f"氐宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{alpha1_lib_coord.ra}, 赤緯為{alpha1_lib_coord.dec}。")
#print(f"房宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{pi_scorpii_coord.ra}, 赤緯為{pi_scorpii_coord.dec}。")
#print(f"心宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{alpha_Scorpii_coord.ra}, 赤緯為{alpha_Scorpii_coord.dec}。")
#print(f"尾宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{mu1_scorpii_coord.ra}, 赤緯為{mu1_scorpii_coord.dec}。")
#print(f"箕宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{gamma2_sagittarii_coord.ra}, 赤緯為{gamma2_sagittarii_coord.dec}。")
#print(f"斗宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{phi_sagittarii_coord.ra}, 赤緯為{phi_sagittarii_coord.dec}。")
#print(f"牛宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{beta_capricorni_coord.ra}, 赤緯為{beta_capricorni_coord.dec}。")
#print(f"女宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{epsilon_aquarii_coord .ra}, 赤緯為{epsilon_aquarii_coord.dec}。")
#print(f"虛宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{beta_aquarii_coord.ra}, 赤緯為{beta_aquarii_coord.dec}。")
#print(f"危宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{alpha_Aquarii_coord.ra}, 赤緯為{alpha_Aquarii_coord.dec}。")
#print(f"室宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{alpha_pegasi_coord.ra}, 赤緯為{alpha_pegasi_coord.dec}。")
#print(f"壁宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{gamma_pegasi_coord.ra}, 赤緯為{gamma_pegasi_coord.dec}。")
#print(f"奎宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{eta_andromedae_coord.ra}, 赤緯為{eta_andromedae_coord.dec}。")
#print(f"婁宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{beta_arietis_coord.ra}, 赤緯為{beta_arietis_coord.dec}。")
#print(f"胃宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{arietis35_coord.ra}, 赤緯為{arietis35_coord.dec}。")
#print(f"昴宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{tauri17_coord.ra}, 赤緯為{tauri17_coord.dec}。")
#print(f"畢宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{epsilon_tauri_coord.ra}, 赤緯為{epsilon_tauri_coord.dec}。")
#print(f"觜宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{lambda_orionis_coord.ra}, 赤緯為{lambda_orionis_coord.dec}。")
#print(f"参宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{zet_Ori_A_coord.ra}, 赤緯為{zet_Ori_A_coord.dec}。")
#print(f"井宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{mu_gem_coord.ra}, 赤緯為{mu_gem_coord.dec}。")
#print(f"鬼宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{theta_cancri_coord.ra}, 赤緯為{theta_cancri_coord.dec}。")
#print(f"柳宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{delta_hydrae_coord.ra}, 赤緯為{delta_hydrae_coord.dec}。")
#print(f"星宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{alphard_coord.ra}, 赤緯為{alphard_coord.dec}。")
#print(f"張宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{upsilon1_hydrae_coord.ra}, 赤緯為{upsilon1_hydrae_coord.dec}。")
#print(f"翼宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{alpha_crateris_coord.ra}, 赤緯為{alpha_crateris_coord.dec}。")
#print(f"軫宿一在 {year}年-{month}月-{day}日 - {hour}:{minute}:{second}的赤經為{gamma_corvi_coord.ra}, 赤緯為{gamma_corvi_coord.dec}。")
