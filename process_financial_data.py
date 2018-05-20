#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 19 16:58:21 2018

@author: aggreymuhebwa
"""

import geopandas as gpd
from shapely.geometry import shape
import pandas as pd
import os
from rtree import index
import matplotlib.pyplot as plt


def load_shapefile(fpath):
    fileName = os.path.join(os.getcwd(), fpath)
    dataset = gpd.read_file(fileName)
    return dataset


def create_lookuptable(_constituences):
    index_table = index.Index()
    for row_id, row in _constituences.iterrows():
        bounds = shape(row['geometry']).bounds
        index_table.insert(row_id, bounds)
    return index_table


def lookup_geopoint(dataset, lookup_table):
    cols = dataset.columns
    final_df = pd.DataFrame(columns=list(cols))
    for i, i_row in dataset.iterrows():
        point = shape(i_row['geometry'])
        for j in list(index_table.intersection(point.coords[0])):
            constituence_poly = constituences.loc[j]['geometry']
            if (point.within(constituence_poly)):
                constituence_name = constituences.loc[j]['CONSTITUEN']
                i_row['geometry'] = shape(constituence_poly)
                xc = i_row.values.reshape(-1, len(i_row))
                temp_df = pd.DataFrame(xc, columns=cols)
                temp_df['CONSTITUEN'] = constituence_name
                temp_df['Count'] = 1
                final_df = pd.concat([final_df, temp_df])
    return final_df


def count_of_finservices(dataset):
    dataset.drop(['County', 'geometry'], inplace=True, axis=1)
    dataset = gpd.GeoDataFrame(dataset, crs={'init': 'epsg:4326'})
    dataset = dataset.groupby('CONSTITUEN').count()
    dataset = dataset.reset_index()
    return dataset


def mergecleaned_dataset_constnces(dataset, constituences):
    merged_result = gpd.GeoDataFrame(pd.merge(constituences, dataset, on='CONSTITUEN'))
    merged_result.crs = {'init': 'epsg:4326'}
    return merged_result


def map_finservices(dataset, constituences, map_title):
    constituences.crs = {'init': 'epsg:4326'}
    base = constituences.plot(color='white', edgecolor='darkgray', figsize=(15, 10))
    dataset.plot(ax=base, column='Count', scheme="equal_interval", legend=True, figsize=(15, 10))
    plt.title('{} {}'.format('Distribition of ', map_title))
    plt.axis('off')
    figname = os.path.join(os.getcwd(), '{}{}.{}'.format('finservices_images/', map_title, 'pdf'))
    plt.savefig(figname, bbox_inches='tight')


def combine_all_finservices(dfames):
    all_finservices = pd.concat(dfames)
    all_finservices = all_finservices.reset_index(drop=True)
    all_finservices = all_finservices.groupby(['CONSTITUEN']).agg('sum')
    all_finservices = all_finservices.reset_index()
    return all_finservices


saccos_shp = load_shapefile('saccos_geo/saccos.shp')
microbanks_shp = load_shapefile('microfinance_banks_geo/microfinance_banks.shp')
atm_machines_shp = load_shapefile('atm_geo/atm_machines.shp')
microinstitutions_shp = load_shapefile('microfinance_institutions_geo/microfinance_institutions.shp')

saccos = saccos_shp[['County', 'geometry']]
microbanks = microbanks_shp[['County', 'geometry']]
atm_machines = atm_machines_shp[['County', 'geometry']]
microinstitutions = microinstitutions_shp[['County', 'geometry']]

constituences = load_shapefile('constituencies/constituencies.shp')
constituences = constituences[['CONSTITUEN', 'geometry']]

# Create an index table/ look-up table for the consistuencies
index_table = create_lookuptable(constituences)

saccos = lookup_geopoint(saccos, index_table)
saccos = count_of_finservices(saccos)

microbanks = lookup_geopoint(microbanks, index_table)
microbanks = count_of_finservices(microbanks)

atm_machines = lookup_geopoint(atm_machines, index_table)
atm_machines = count_of_finservices(atm_machines)

microinstitutions = lookup_geopoint(microinstitutions, index_table)
microinstitutions = count_of_finservices(microinstitutions)

# combine all financial services
dfames = [saccos, microbanks, atm_machines, microinstitutions]
all_finservices = combine_all_finservices(dfames)
all_finservices.to_csv('clean_financialdata/combined_financialservices.csv', index=False)

saccos = mergecleaned_dataset_constnces(saccos, constituences)
map_finservices(saccos, constituences, 'SACCOS')

microbanks = mergecleaned_dataset_constnces(microbanks, constituences)
map_finservices(microbanks, constituences, 'Microfinance_banks')

atm_machines = mergecleaned_dataset_constnces(atm_machines, constituences)
map_finservices(atm_machines, constituences, 'ATM_Machines')

microinstitutions = mergecleaned_dataset_constnces(microinstitutions, constituences)
map_finservices(microinstitutions, constituences, 'Microfinance_institutions')

all_finservices = mergecleaned_dataset_constnces(all_finservices, constituences)
map_finservices(all_finservices, constituences, 'All_Financial_services')
