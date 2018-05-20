#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 09:37:47 2018

@author: aggreymuhebwa
"""
import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pylab import *
import seaborn as sns
import numpy as np

'''
Fix constituence names in the census data, merge with the constituences shape file
and generate a shape file of the combined data. 
'''
def load_dataset(fpath):
    fileName = os.path.join(os.getcwd(), fpath)
    dataset = pd.read_csv(fileName)
    return dataset


def load_shapefile(fpath):
    fileName = os.path.join(os.getcwd(), fpath)
    dataset = gpd.read_file(fileName)
    return dataset


def fix_constituences(clean_file, file_tofix):
    file_tofix['Constituency'] = clean_file['Constituency']
    return file_tofix


def merge_datasets(_constituences, dataset):
    dataset = dataset.rename(columns={'Constituency': 'CONSTITUEN'})
    dataset['CONSTITUEN'] = dataset['CONSTITUEN'].str.upper()
    merged_result = pd.merge(constituences, dataset, on='CONSTITUEN')
    return merged_result


def plot_maps(constituences, dataset, cmap, sectorname):
    dataset.crs = {'init': 'epsg:4326'}  # set projection
    constituences.crs = {'init': 'epsg:4326'}
    allColumns = dataset.columns.values
    ignore_columns = ['COUNTY_NAM', 'CONSTITUEN', 'geometry', 'County']
    for column_name in allColumns:
        if column_name in ignore_columns:
            pass
        else:
            base = constituences.plot(color='white', linewidth=1.0, edgecolor='darkgray', figsize=(15, 10))
            dataset.plot(ax=base, column=column_name, cmap=cmap, scheme='equal_interval', legend=True)
            plt.title('{} {}'.format('Distribition of ', column_name))
            plt.axis('off')
            figname = os.path.join(os.getcwd(), '{}{}_{}.{}'.format('census_images/', sectorname, column_name, 'pdf'))
            plt.savefig(figname, bbox_inches='tight')


def plot_heatmap(dataset, sectorname, cmap):
    dataset = dataset.drop(columns={'CONSTITUEN', 'geometry', 'COUNTY_NAM'}, axis=1)
    dataset = dataset.groupby('County').mean()
    dataset = dataset.transpose()
    corr = dataset.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.heatmap(corr, mask=mask, cmap=cmap)
    plt.title('{} {} {}'.format('Heatmap showing correlation for ', sectorname, 'sector'))
    figname = os.path.join(os.getcwd(), '{}{}_{}.{}'.format('census_images/', sectorname, 'heatmap', 'pdf'))
    plt.savefig(figname, bbox_inches='tight')


constituences = load_shapefile('constituencies/constituencies.shp')
wastedisposal = load_dataset('cleaned_censusdata/wastedisposal.csv')
cookingfuel = load_dataset('cleaned_censusdata/cookingfuel.csv')
employment = load_dataset('cleaned_censusdata/employment.csv')

# fix the constituency column for the remaining dataset
cookingfuel = fix_constituences(wastedisposal, cookingfuel)
employment = fix_constituences(wastedisposal, employment)

constituences = constituences[['COUNTY_NAM', 'CONSTITUEN', 'geometry']]

wastedisposal = merge_datasets(constituences, wastedisposal)
cookingfuel = merge_datasets(constituences, cookingfuel)
employment = merge_datasets(constituences, employment)

plot_maps(constituences, wastedisposal, 'Blues', 'wastedisposal')
plot_maps(constituences, cookingfuel, 'OrRd', 'cookingfuel')
plot_maps(constituences, employment, 'RdPu', 'employment')

plot_heatmap(employment, 'Employment', 'Greens')
plot_heatmap(cookingfuel, 'cookingfuel', 'Reds')
plot_heatmap(wastedisposal, 'wastedisposal', 'Blues')
