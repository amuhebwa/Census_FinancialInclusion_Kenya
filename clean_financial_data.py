#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 12:10:00 2018

@author: aggreymuhebwa
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

'''
Python code to extract only the required data from the financial inclusion datasets, save a copy to
a csv file and generate shape files
'''
def save_shapefiles(data, filename):
    points = [Point(row['GPS Longitude'], row['GPS Latitude']) for row_id, row in data.iterrows()]
    tempfile = gpd.GeoDataFrame(data, geometry=points)
    tempfile.to_file(filename, driver='ESRI Shapefile')


def save_csvfile(data, filename):
    data.to_csv(filename, index=False)


saccos = pd.read_csv('saccos.csv', usecols=['County', 'GPS Latitude', 'GPS Longitude'], low_memory=False)
microfinance_banks = pd.read_csv('microfinance_banks.csv', usecols=['County', 'GPS Latitude', 'GPS Longitude'],
                                 low_memory=False)
atm_machines = pd.read_csv('atm_machines.csv', usecols=['County', 'GPS Latitude', 'GPS Longitude'], low_memory=False)
microfinance_institutions = pd.read_csv('microfinance_institutions.csv',
                                        usecols=['County', 'GPS Latitude', 'GPS Longitude'], low_memory=False)

save_csvfile(saccos, 'clean_financialdata/saccos.csv')
save_csvfile(microfinance_banks, 'clean_financialdata/microfinance_banks.csv')
save_csvfile(atm_machines, 'clean_financialdata/atm_machines.csv')
save_csvfile(microfinance_institutions, 'clean_financialdata/microfinance_institutions.csv')

save_shapefiles(saccos, 'saccos_geo/saccos.shp')
save_shapefiles(microfinance_banks, 'microfinance_banks_geo/microfinance_banks.shp')
save_shapefiles(atm_machines, 'atm_geo/atm_machines.shp')
save_shapefiles(microfinance_institutions, 'microfinance_institutions_geo/microfinance_institutions.shp')
