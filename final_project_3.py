# IMPORT STATEMENTS

# UNITTEST AND SYSTEM IMPORTS
import unittest
import sys

# GENERAL REQUEST / JSON IMPORTS
import requests
import json

# API / DATA COLLECTING WRAPPERS
import omdb
import wikipedia

# DATABASE TOOLS
import sqlite3
import collections
import itertools

#____________________________________________________________________________________________________

# SETTING UP CACHE

CACHE_FNAME = "SI206_final_project_cache.json"

try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}

#____________________________________________________________________________________________________

# PULLING MOVIE SUGGESTIONS FROM OMDB

def get_movies(user_query):

    # IF INPUTTED SEARCH QUERY IS CACHED
	if user_query in CACHE_DICTION:
		print("\nGetting movie suggestions from cached data...")

		# GETTING WIKI SUGGESTIONS FROM CACHE DICTIONARY
		movie_data = CACHE_DICTION[user_query]

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

	# IF INPUTTED SEARCH QUERY IS NOT CACHED --- PULLING FROM WEB

	else:
		print("\nRetrieving movie suggestions from web...")

		# GETTING WIKI SUGGESTIONS
		movie_data = omdb.title(user_query)

		# CACHING LIST OF SUGGESTIONS
		CACHE_DICTION[user_query] = movie_data

	cached_suggs = open(CACHE_FNAME, 'w')
	cached_suggs.write(json.dumps(CACHE_DICTION))
	cached_suggs.close()

	# RETURNING DICTIONARY OF SUGGESTIONS
	return movie_data

#____________________________________________________________________________________________________

# Running get_movies function based on user input

in1 = input("Enter a movie title:  \n")
getting_movie = get_movies(in1)
# getting_movie is a dictionary of info for the single movie inputted

# print(getting_movie) WORKING --> prints a dict of movie info

#____________________________________________________________________________________________________

# CREATING A CLASS MOVIE

class Movie(object):
	def __init__(self, getting_movie):
		self.title = getting_movie["title"]
		self.director = getting_movie["director"]
		self.writer = getting_movie["writer"]
		self.plot = getting_movie["plot"]
		self.rating = getting_movie["imdb_rating"]

	def __str__(self):
		stringformation = (self.title, self.plot, self.rating)
		return "Movie Title: {}\nSynopsis: {}\nIMBD Rating: {}\n".format(stringformation)

	def print_all_data(self):
		a = "Movie Title: {}\n".format(self.title)
		b = "Synopsis: {}\n".format(self.plot)
		c = "IMDB Rating: {}\n".format(self.rating)
		d = "Director: {}\n".format(self.director)
		e = "Writer: {}\n".format(self.writer)
		return a+b+c+d+e

	def get_director(self):
		return self.director

	def get_writer(self):
		return self.writer

my_movie = Movie(getting_movie) # Making an instance of getting_movie dict 

# GETTING A STRING OF THE DIRECTOR AND WRITER'S NAMES

movie_director = my_movie.get_director()
print(movie_director)

movie_writer = my_movie.get_writer()
print(movie_writer)

#____________________________________________________________________________________________________

# PULLING SUGGESTIONS FROM WIKIPEDIA

def get_wiki_suggs(input_q):

    # IF INPUTTED SEARCH QUERY IS CACHED
	if input_q in CACHE_DICTION:
		print("\nGetting Wikipedia suggestions from cached data...")

		# GETTING WIKI SUGGESTIONS FROM CACHE DICTIONARY
		wiki_dict = CACHE_DICTION[input_q]

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

	# IF INPUTTED SEARCH QUERY IS NOT CACHED --- PULLING FROM WEB

	else:
		print("\nRetrieving Wikipedia suggestions from web...")

		if "," in input_q:
			names = input_q.split(',')
			main_director_or_writer = names[0]
			# Getting suggestions for wiki page of the MAIN director / writer (in the case that there are two)
			wiki_suggs = wikipedia.search(main_director_or_writer)
			# Getting full wiki page
			wiki_page = wikipedia.WikipediaPage(wiki_suggs[0])

		else:
			# Getting suggestions of wiki page
			wiki_suggs = wikipedia.search(input_q)
			# Getting full page
			wiki_page = wikipedia.WikipediaPage(wiki_suggs[0])

		# CREATING DICTIONARY OF WIKI PAGE DATA
		# BECAUSE WIKI_PAGE IS A CLASS OBJECT 
		# ---> TRANSFERRING INFO I WANT TO A CACHABLE OBJECT (a dicitonary --> wiki_dict)
 
		wiki_dict = {}
		wiki_dict["summary"] = wiki_page.summary # a string
		wiki_dict["categories"] = wiki_page.categories # a list of strings
		wiki_dict["links"] = wiki_page.links # a list of strings
		wiki_dict["sections"] = wiki_page.sections # a list of strings
		wiki_dict["content"] = wiki_page.content

		# CACHING LIST OF SUGGESTIONS
		CACHE_DICTION[input_q] = wiki_dict

	cached_suggs = open(CACHE_FNAME, 'w')
	cached_suggs.write(json.dumps(CACHE_DICTION))
	cached_suggs.close()

	# RETURNING DICTIONARY OF SUGGESTIONS
	return wiki_dict

#____________________________________________________________________________________________________

# DEFINING FUNCTION TO INVOKE GET_WIKI_SUGGS FUNCTION

def get_wiki(person):
	try:
		person_info = get_wiki_suggs(person)
		return person_info
	except:
		# TO PREVENT DISAMBIGUOUS ERRORS
		print("\n\nOops! We don't seem to have the director and writer of that movie in our database. Please try again with another movie.\n")
		sys.exit()

# INVOKING GET_WIKI FUNCTION ON THE DIRECTOR AND WRITER NAMES

director_wiki = get_wiki(movie_director)
writer_wiki = get_wiki(movie_writer)

#____________________________________________________________________________________________________

# CREATING CLASS WIKIPAGE

class Wikipage(object):
	def __init__(self, dict1):
		self.summary = dict1["summary"]
		self.categories = dict1["categories"]
		self.links = dict1["links"]
		self.sections = dict1["sections"]
		self.content = dict1["content"]

	def printable_list(self):
		print("\nDirector background information:  \n" + self.summary)
		print("\nSimilar pages: ")
		for link in self.links[:6]:
			print(link)
		print("\nCategories: ")
		for category in self.categories[:6]:
			print(category)

	def getting_all_content(self):
		a = "Background Information: "
		b = self.summary

		c = "Complete Wikipedia Page: "
		d = self.content

		print(a+b+c+d)

#____________________________________________________________________________________________________

# CREATING TWO CLASS WIKIPAGE INSTANCES: ONE FOR THE DIRECTOR AND ONE FOR THE WRITER

director_instance = Wikipage(director_wiki)
writer_instance = Wikipage(writer_wiki)

director_instance.printable_list()

#printable_list(director_instance)

#_____________________________________________________________________________________________________














