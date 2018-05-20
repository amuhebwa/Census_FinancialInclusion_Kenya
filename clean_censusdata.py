#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 12:11:26 2018

@author: aggreymuhebwa
"""

import pandas as pd
import wastedisposal as wdisposal
import cookingfuel as cfuel
import empl as employment

''''
Python code to extract census data from python files and save in csv format
'''
# Error concatenating file path with the object to be accessed
# Not top priority, so replicating the data loading function
def load_data_empl(fileName):
    columns = fileName.emplcols
    data = fileName.empl
    match_on = 'Constituency'
    final_df = pd.DataFrame(columns=columns)
    index = -1
    for key in data.keys():
        for admin_level in data[key][0]:
            index = index + 1
            if match_on in admin_level:
                constituency_data = data[key][1][index]
                xc = constituency_data.reshape(-1, len(constituency_data))
                temp_df = pd.DataFrame(xc, columns=columns)
                temp_df['County'] = key
                temp_df['Constituency'] = admin_level[:-12]
                final_df = pd.concat([final_df, temp_df])
        index = 0
    return final_df.reset_index(drop=True)


def load_data_cfuel(fileName):
    columns = fileName.cookingfuelcols
    data = fileName.cookingfuel
    match_on = 'Constituency'
    final_df = pd.DataFrame(columns=columns)
    index = -1
    for key in data.keys():
        for admin_level in data[key][0]:
            index = index + 1
            if match_on in admin_level:
                constituency_data = data[key][1][index]
                xc = constituency_data.reshape(-1, len(constituency_data))
                temp_df = pd.DataFrame(xc, columns=columns)
                temp_df['County'] = key
                temp_df['Constituency'] = admin_level[:-12]
                final_df = pd.concat([final_df, temp_df])
        index = 0
    return final_df.reset_index(drop=True)


def load_data_wdisposal(fileName):
    columns = fileName.wastedisposalcols
    data = fileName.wastedisposal
    match_on = 'Constituency'
    final_df = pd.DataFrame(columns=columns)
    index = -1
    for key in data.keys():
        for admin_level in data[key][0]:
            index = index + 1
            if match_on in admin_level:
                constituency_data = data[key][1][index]
                xc = constituency_data.reshape(-1, len(constituency_data))
                temp_df = pd.DataFrame(xc, columns=columns)
                temp_df['County'] = key
                temp_df['Constituency'] = admin_level[:-12]
                final_df = pd.concat([final_df, temp_df])
        index = 0
    return final_df.reset_index(drop=True)


employment = load_data_empl(employment)
cookingfuel = load_data_cfuel(cfuel)
wastedisposal = load_data_wdisposal(wdisposal)
employment.to_csv('cleaned_censusdata/employment1.csv', index=False)
cookingfuel.to_csv('cleaned_censusdata/cookingfuel1.csv', index=False)
wastedisposal.to_csv('cleaned_censusdata/wastedisposal1.csv', index=False)
