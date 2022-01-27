#import contextily as ctx
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import requests
import calendar
import geopandas as gpd
import os.path as os
import scipy.stats
import seaborn.palettes
import seaborn.utils
import sys
from census import Census
from us import states
import http.client, urllib.request, urllib.parse, urllib.error, base64

root= r"C:/Users/Jennah/Desktop/Code/nyc_fire_risk"

url_2020= "https://data.cityofnewyork.us/resource/usc3-8zwd.csv?$limit=100000"
url_2019= "https://data.cityofnewyork.us/resource/wcm8-aq5w.csv?$limit=100000"
url_2018= "https://data.cityofnewyork.us/resource/4tys-3tzj.csv?$limit=100000"
url_2017= "https://data.cityofnewyork.us/resource/4t62-jm4m.csv?$limit=100000"

urls= [url_2017, url_2018, url_2019, url_2020]
cols= [["property_id", "year_ending",\
                                      "property_name", "nyc_borough_block_and_lot",\
                                      "occupancy", "year_built", "number_of_buildings",\
                                       "water_use_all_water_sources", "multifamily_housing_number"],\
      ["property_id", "year_ending",\
                                      "property_name", "nyc_borough_block_and_lot",\
                                      "occupancy", "year_built", "number_of_buildings",\
                                       "water_use_all_water_sources", "multifamily_housing_number"],\
      ["property_id", "year_ending",\
                                      "property_name", "nyc_borough_block_and_lot",\
                                      "occupancy", "year_built", "number_of_buildings",\
                                       "water_use_all_water_sources", "multifamily_housing_number"],\
      ["property_id", "year_ending",\
                                      "property_name", "nyc_borough_block_and_lot_bbl",\
                                      "occupancy", "year_built", "number_of_buildings",\
                                       "water_use_all_water_sources_kgal", "multifamily_housing_number_of_bedrooms"]]
dfs= [pd.read_csv(urls[i], usecols = cols[i]) for i in range(0, len(urls))]
dfs

dfs[0].columns = cols[0]
dfs[1].columns = cols[0]
dfs[2].columns = cols[0]
dfs[3].columns = cols[0]

df_ew= pd.concat(dfs, axis = 0)
df_ew

df_ew["nyc_borough_block_and_lot"]= df_ew["nyc_borough_block_and_lot"].to_string()
df_ew["bbl"]= df_ew["nyc_borough_block_and_lot"].str.replace("[A-z]{1}[0-9]{3}-", "", regex = True)
df_ew["bbl"]= df_ew["bbl"].str.replace("-", "")
df_ew["bbl"]= df_ew["bbl"].str.replace(" ", ";")
df_ew["bbl"]= df_ew["bbl"].str.replace("(?<=[0-9]{10})/", ";", regex = True)
df_ew["bbl"]= df_ew["bbl"].str.replace("/", "")
df_ew["bbl"]= df_ew["bbl"].str.replace(",", ";")
df_ew["bbl"]= df_ew["bbl"].str.replace(":", ";")
df_ew["bbl"]= df_ew["bbl"].str.replace("and", ";")
df_ew["bbl"]= df_ew["bbl"].str.replace("&", ";")
df_ew["bbl"]= df_ew["bbl"].str.replace("NotAvailable", "")
df_ew["bbl"]= df_ew["bbl"].str.replace("multiple", "")

df_ew[["bbl" + str(i) for i in range(0, 42)]]= df_ew["bbl"].str.split(pat= ";", n=-1, expand = True)
df_ew.loc[df_ew["bbl"].map(len) > 10, ["nyc_borough_block_and_lot", "bbl0", "bbl1", "address_1", "address_2", "city"]]
