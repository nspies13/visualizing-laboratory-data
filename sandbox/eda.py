#%%

import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt  
import numpy as np

def import_data(path):
    df=pd.read_csv(path)
    return(df)

def import_geodata(path):
    gdf=gpd.read_file(path)
    return(gdf)

def clean_df_od(df):
    df['FIPS'] = df['FIPS'].apply(lambda x: f"{x:05}" if x < 10000 else str(x))
    df['AFFGEOID']= '0500000US' + df['FIPS'].astype(str)
    df['Provisional Drug Overdose Deaths']=np.where(df['Provisional Drug Overdose Deaths'].isna(),0,df['Provisional Drug Overdose Deaths'])
    df['Provisional Drug Overdose Deaths'] = df['Provisional Drug Overdose Deaths'].str.replace(',', '').astype(float)
    return(df)

def main():
    df_pop=import_data('ACSDP5Y2022.DP05-Data.csv')
    df_od=import_data('VSRR_Provisional_County-Level_Drug_Overdose_Death_Counts.csv')
    gdf=import_geodata('cb_2018_us_county_500k/cb_2018_us_county_500k.shp')
    gdf_conn=import_geodata('Connecticut_Planning_Region_Index_-4068945793831471951/deepgis_DEEP_PLANNING_REGION_INDEX.shp')
    gdf=gdf[(gdf.STATEFP != '66')&(gdf.STATEFP != '60')&(gdf.STATEFP != '69') &
    (gdf.STATEFP != '78')&(gdf.STATEFP != '72')]
    gdf=gdf.to_crs("EPSG:4269")
    gdf_conn=gdf_conn.to_crs("EPSG:4269")
    gdf_conn['AFFGEOID']=df_pop[df_pop.NAME.str.contains('conn',case=False)]['GEO_ID'].to_list()
    gdf=pd.concat([gdf,gdf_conn])
    dff_od=clean_df_od(df_od)
    df_od_sum=dff_od.groupby('AFFGEOID')['Provisional Drug Overdose Deaths'].sum().reset_index()
    gdff=pd.merge(gdf,df_od_sum,on='AFFGEOID',how='left')
    return(gdff)

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
    
#%%
gdf=main()