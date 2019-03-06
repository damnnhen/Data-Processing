#!/usr/bin/env
# Name: Daniel Hendriks
# Student number: 11419628
"""
This script creates a dataframe and visualizes variables in the dataframe and outputs a JSON file 
"""

#import libraries
import pandas as pds
import csv
from contextlib import closing
from numpy import percentile
import matplotlib.pyplot as plt
import re

input_file = 'input.csv'
csv_output = 'output.csv'
json_output = 'data.json'

#determine column names that will be used in functions
country = "Country"
region = "Region"
pop_density = "Pop. Density (per sq. mi.)"
inf_mortality = "Infant mortality (per 1000 births)"
gdp = "GDP ($ per capita) dollars"
all_cols = ['Country', 'Region', 'Pop. Density (per sq. mi.)','Infant mortality (per 1000 births)', 'GDP ($ per capita) dollars']


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
def save_json(df, column_index):

    # sorted on specified column
    df = df.set_index([column_index])
    output = df.to_json(orient='index')
    with open(json_output, 'w') as j:
        j.write(output)

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

# replace comma's with decimal points
def decimal_point(df, *columns):

    # replace per column
    for column in columns:
        df[column] = df[column].str.replace(',', '.')
    
    return df

# remove specific word
def remove_word(df, column, word):
    
    # Remove word at end, from specified column
    df[column] = df[column].str.rstrip(word)
    return df

# determine range
def determine_range(df, low_statistical_cutoff, high_statistical_cutoff, *columns):

    for column in columns:
        df[column] = df[column][df[column].between(df[column].quantile(low_statistical_cutoff), df[column].quantile(high_statistical_cutoff))]
    
    return df    

def to_num(df, *columns):

    for column in columns:
            df[column] = df[column].apply(pds.to_numeric, errors ='ignore')
    return df

# calculate central tendency/centrality and print out string with values
def centrality(df, column):
    
    mode_column = df[column].mode()[0]
    median_column = df[column].median()
    mean_column = df[column].mean()
    std_column = df[column].std()

    stats = [mean_column, median_column, mode_column, std_column]
    print("\n Normality Indicators\n Mean:", stats[0], "\n Median", stats[1], "\n Mode:", stats[2], "\n Standard Deviation:", stats[3])

# calculate five number summary and print out string with values
def five_stats(df, low_statistical_cutoff, high_statistical_cutoff, *columns):

    for column in columns: 
        median_column = df[column].median()
        min_column = df[column].min()
        Q1_column = df[column].quantile(low_statistical_cutoff)
        Q3_column = df[column].quantile(high_statistical_cutoff)
        max_column = df[column].max()

        stats = [min_column, Q1_column, median_column, Q3_column, max_column]
        print("\n Five Number Summary of ", column, "\n Min:", stats[0], "\n Quantile 1:", stats[1], "\n Median:", stats[2], "\n Quantile 3:", stats[3], "\n Max:", stats[4])

def plot_graph(df, column, type, title):
    
    # Create graph from column and show
    if type == 'histogram':
        graph = df[column].plot.hist()
        graph.set_title(title)
    elif type == 'boxplot':
        graph = df[column].plot.box()
        graph.set_title(title)
    else:
        return
    
    plt.show()


if __name__ == "__main__":

    # Load dataset into dataframe
    df = load_data(input_file)

    # Select columns
    df = filter_cols(df, country, region, pop_density, inf_mortality, gdp)

    print(df)

    # get decimal point 
    df = decimal_point(df, pop_density, inf_mortality)

    print(df)
    # drop missing
    df = drop_missing(df)

    print(df)

    # remove specific word
    df = remove_word(df, gdp, "dollars")

    # remove redundant space after region
    remove_space(df, region)

    # convert to numbers to make calculations on
    df = to_num(df, gdp, pop_density, inf_mortality)

    # determine range
    df = determine_range(df, 0.01, 0.99, pop_density, gdp, inf_mortality)

    print(df)

    # check centrality indicators
    centrality(df, gdp)

    # print five key statistics
    five_stats(df, 0.25, 0.75, inf_mortality, gdp)

    # debug
    print(df)

    # Print histogram for GDP and boxplot for Infant Mortality
    plot_graph(df, gdp, "histogram", "GDP Distribution")
    plot_graph(df, inf_mortality, "boxplot", "Infant Mortality frequency")

    # Save df in json 
    save_json(df, country)

    # debug
    print(df)
