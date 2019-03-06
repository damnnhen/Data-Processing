#!/usr/bin/env
# Name: Daniel Hendriks
# Student number: 11419628
"""
This script converts a CSV file to a JSON file
The data will be used to show the trend of Dutch speed skating medals 
"""

#import libraries
import pandas as pds
import csv
from contextlib import closing
from numpy import percentile
import matplotlib.pyplot as plt
import re
import numpy as np
from csv import reader
import json
from json import dump
import itertools

input_file = 'athlete_events.csv'
csv_output = 'output.csv'
json_output = 'dutch_winterolympics_medals.json'

#determine column names that will be used in functions
ID = "ID"
country_code = "NOC"
name = "Name"
year = "Year"
season = "Season"
sport = "Sport"
medal = "Medal"
random = 'Unique'
all_cols = ['NOC', 'Year', 'Season','Sport', 'Medal', 'Name' 'ID']

start_year = min(year)
end_year = max(year)

def get_nested_rec(key, grp):
    rec = {}
    rec['NOC'] = key[0]
    rec['Year'] = key[1]
    rec['Season'] = key[2]
    rec['Sport'] = key[3]
 
    for var in ['Medal','Name']:
        rec[var] = list(grp[var])

    return rec

# load CSV file with pandas
def load_data(file):
    
    # Load data into dataframe
    df = pds.read_csv(file)
    return df

# remove redundant space that will be shown otherwise in JSON
def remove_space(df, column):
    
    df[column] = df[column].str.strip()
    return df

# save as JSON
def save_json(df):

    with open(json_output, 'w') as fp:
        json.dump(records, fp, sort_keys=True, indent=4)

# select the columns to be remained
def filter_cols(df, *columns):

    # convert specified columns to list 
    df = df[list(columns)]
    return df

# drop missing values
def drop_missing(df):

    # drop values 'unknown'
    df = df[df != 'unknown']
    # drop na 
    df = df.dropna()
    return df


def mask_standard(df):
    new = df['NOC'] == "NED"
    df = df[new]
    new2 = df['Sport'] == "Speed Skating"
    df = df[new2]
    return df


def myconverter(o):
    if isinstance(o, np.float64):
        return int(o)

def count_in_array(df, column):

    df[column] = list.count((df[column]))
    return df

def tolist(df, column):
    
    df[column] = df[column].tolist()
    return df


if __name__ == "__main__":

    # Load dataset into dataframe
    df = load_data(input_file)

    # Select columns
    df = filter_cols(df, country_code, year, season, sport, medal, name)

    df = mask_standard(df)

    df = drop_missing(df)

    records = []

    for key, grp in df.groupby(['NOC','Year','Season', 'Sport']):
        rec = get_nested_rec(key, grp)
        records.append(rec)

    records = dict(data = records)

    df = pds.DataFrame(records)

    df.to_json(path_or_buf='df.json')

    print(df)

    keyCount = len(rec['Medal'])
    print(keyCount)



    
    





