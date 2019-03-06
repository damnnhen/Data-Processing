#!/usr/bin/env python
# Name: Daniel Hendriks
# Student number: 11419628
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """

    movie_import = dom.find_all(class_='lister-item-content')

    # create lists 
    title = []
    releaseyear = []
    rating = []
    cast = []
    runtime = []
    everymovie_info = []
    movie_list = []


    # iterate over all movies in movie_import
    for everymovie in movie_import:
        # get title from every movie in movie_import 
        title = everymovie.find('h3', attrs={'class':"lister-item-header"}).a.string
       
        # get year from every movie in movie_import
        releaseyear = everymovie.find('span', attrs={'class':"lister-item-year"}).string[-5:-1]
        releaseyear = int(releaseyear)

        # get rating from every movie in movie_import
        rating = everymovie.find('div', attrs={'class':"inline-block ratings-imdb-rating"}).get_text()[2:5]
        rating = float(rating)


        cast = ", ".join([castmember.string for castmember in everymovie.find('p', attrs={'class':""}).find_all('a')[-4:]])

        # get run-time from every movie in movie_import
        runtime = everymovie.find('span', attrs={'class':"runtime"}).string[:-4]

        # variable list in movie_list 
        movie_list.append([title, releaseyear, rating, cast, runtime])


    return movie_list 


def save_csv(outfile, movie_list):

    #write csv with header
    writer = csv.writer(outfile, delimiter='\t')
    writer.writerow(['Title', 'Year', 'Rating', 'Cast', 'Runtime'])

    # put movies in rows
    for everymovie in movie_list:
        writer.writerow(everymovie)
   

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movie_list = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movie_list)