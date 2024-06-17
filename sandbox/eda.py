#%%

import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt  

#%%
df_pop=pd.read_csv('ACSDP5Y2022.DP05-Data.csv')

#%%
df_od=pd.read_csv('VSRR_Provisional_County-Level_Drug_Overdose_Death_Counts.csv')

#%%
gdf=gpd.read_file('cb_2018_us_county_500k/cb_2018_us_county_500k.shp')
gdf=gdf[(gdf.STATEFP != '66')&(gdf.STATEFP != '60')&(gdf.STATEFP != '69') &
    (gdf.STATEFP != '78')&(gdf.STATEFP != '72')]

#%%
# gdf=gdf.to_crs("ESRI:102003")
gdf=gdf.to_crs("EPSG:4269")

#%%
fig, continental_ax = plt.subplots(figsize=(20, 10))
alaska_ax = continental_ax.inset_axes([.08, .01, .20, .28])
hawaii_ax = continental_ax.inset_axes([.28, .01, .15, .19])
# gdf.plot(ax=continental_ax)

alaska_ax.set_ylim(51, 72)
alaska_ax.set_xlim(-180, -127)

hawaii_ax.set_ylim(18.8, 22.5)
hawaii_ax.set_xlim(-160, -154.6)

vmin, vmax = gdf['ALAND'].agg(['min', 'max'])
gdf[(gdf.STATEFP!='15')&(gdf.STATEFP!='02')].plot(ax=continental_ax, vmin=vmin, vmax=vmax)
gdf.loc[gdf.STATEFP=='02'].plot(ax=alaska_ax, vmin=vmin, vmax=vmax)
gdf.loc[gdf.STATEFP=='15'].plot(ax=hawaii_ax, vmin=vmin, vmax=vmax)

for ax in [continental_ax, alaska_ax, hawaii_ax]:
    ax.set_yticks([])
    ax.set_xticks([])