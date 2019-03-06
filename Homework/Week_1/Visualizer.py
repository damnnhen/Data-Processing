#!/usr/bin/env python
# Name: Daniel Hendriks
# Student number: 11419628
"""
This script visualizes data obtained from a .csv file
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean

# Global constants for the input file, first and last year
INPUT_CSV = "movies.csv"
START_YEAR = 2008
END_YEAR = 2018

# Global dictionary for the data
data_dict = {str(key): [] for key in range(START_YEAR, END_YEAR)}

# check data_dict
print(data_dict)

# open csv file 
with open(INPUT_CSV, newline='') as csvfile:
    #specify that delimiter is tab
    reader = csv.DictReader(csvfile, delimiter='\t')
    # add rating to the year key
    for row in reader:
        data_dict[str(row["Year"])].append(float(row['Rating']))

# get average rating per year and set to year key
for year_key in range(START_YEAR, END_YEAR):
    ratings = data_dict[str(year_key)]
    average = round(mean(ratings), 1)
    # set rating value associated with year key equal to average rating
    data_dict[str(year_key)] = average

if __name__ == "__main__":

    # Create bar chart
    plt.xlabel('Year')
    plt.ylabel('Rating')
    plt.title('Average yearly rating of IMDB Top 50 movies')
    plt.bar(data_dict.keys(), data_dict.values(), align='center', alpha=1)
    plt.ylim(7.0, 10.0)
    plt.show()
    plt.plot(secondary_y=True)