#!/usr/bin/env python
# Name:
# Student number:
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import re


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

    '''
    #would like to have known whether it would be interesting to create class and how
    # make class that 
    class Movie():
        def __init__(self, movie_title,movie_rating, movie_releaseyear,actors,actresses):
            self.title = movie_title
            self.movie_rating = movie_rating
            self.movie_releaseyear = movie_releaseyear
            self.actors= []
            self.actresses= []

        def AddActor(self, actor):
            self.actors.append(actor)
        def AddActress(self, actress):
            self.actresses.append(actress)
    '''

    movie_import = dom.find_all(class_='lister-item-content')

    #create lists of variables I want to store data in 

    title = []
    releaseyear = []
    rating = []
    cast = []
    runtime = []
    movie_single = []
    movie_list = []


    # iterate over all moveis in movie_import
    for everymovie in movie_import:
        # get title from every movie in movie_import 
        title_iterate = everymovie.h3.a.string
        title.append(title_iterate)
        # get year from
        releaseyear_iterate = everymovie.find(class_='lister-item-year text-muted unbold').string.strip("()")
        releaseyear.append(releaseyear_iterate)

        rating_iterate = everymovie.find(class_='inline-block ratings-imdb-rating').strong.string
        rating.append(rating_iterate)

        for castmember_iterate in everymovie.find_all('a', attrs={'href': re.compile("ref_=adv_li_st_")}):
            cast.append(castmember_iterate.string)

        runtime_iterate = everymovie.find(class_='runtime').string
        runtime.append(runtime_iterate)

        movie_single = [title, releaseyear, rating, cast, runtime]
        movie_list.append(movie_single)



    # ADD YOUR CODE HERE TO EXTRACT THE ABOVE INFORMATION ABOUT THE
    # HIGHEST RATED MOVIES
    # NOTE: FOR THIS EXERCISE YOU ARE ALLOWED (BUT NOT REQUIRED) TO IGNORE
    # UNICODE CHARACTERS AND SIMPLY LEAVE THEM OUT OF THE OUTPUT.

    return [movie_list]   # REPLACE THIS LINE AS WELL IF APPROPRIATE


def save_csv(outfile, movie_import):
    """
    Output a CSV file containing highest rated movies.
    """
    writer = csv.writer(outfile, delimiter=',')
    #write header
    writer.writerow(['title', 'rating', 'releaseyear', 'cast', 'runtime'])
    for movie in movie_import:
        writer.writerow(movie)

    
    ## SOURCE: 
    '''
    for movie_listplace in movie_import[0]:
        # join string of cast 
        cast = ", ".join(map(str, movie_listplace[3]))
        # Here all the information that is needed is printed.
        writer.writerow([movie_listplace[0], movie_listplace[1], movie_listplace[2], cast, movie_listplace[4]])

    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE MOVIES TO DISK
    '''

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
    movie_import = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movie_import)