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

# TASK 1: SETTING UP CACHE

CACHE_FNAME = "SI206_final_cache.json"

try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION2 = json.loads(cache_contents)
except:
	CACHE_DICTION2 = {}

#____________________________________________________________________________________________________

# TASK 2: PULLING MOVIE SUGGESTIONS FROM OMDB

def get_movies(user_query):

    # IF INPUTTED SEARCH QUERY IS CACHED
	if user_query in CACHE_DICTION2:
		#print("\nGetting movie suggestions from cached data...")

		# GETTING WIKI SUGGESTIONS FROM CACHE DICTIONARY
		movie_data = CACHE_DICTION2[user_query]

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

	# IF INPUTTED SEARCH QUERY IS NOT CACHED --- PULLING FROM WEB

	else:
		#print("\nRetrieving movie suggestions from web...")

		# GETTING WIKI SUGGESTIONS
		movie_data = omdb.title(user_query)

		# CACHING LIST OF SUGGESTIONS
		CACHE_DICTION2[user_query] = movie_data

	cached_suggs = open(CACHE_FNAME, 'w')
	cached_suggs.write(json.dumps(CACHE_DICTION2))
	cached_suggs.close()

	# RETURNING DICTIONARY OF SUGGESTIONS
	return movie_data

#____________________________________________________________________________________________________

# TASK 3: Running get_movies function based on input

#in1 = input("\nEnter a movie title:  \n")
in1 = "Harry Potter"
getting_movie_1 = get_movies(in1)

in2 = "Date Night"
getting_movie_2 = get_movies(in2)

in3 = "Now You See Me"
getting_movie_3 = get_movies(in3)

# getting_movie is a dictionary of info for the single movie inputted

# print(getting_movie) WORKING --> prints a dict of movie info

#____________________________________________________________________________________________________

# TASK 4: CREATING CLASS MOVIE

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
		if "," in self.director:
			dir0 = self.director
			dir1 = dir0.split(",")
			dir2 = dir1[0]
			if "(" in dir2:
				dir3 = dir2.split("(")
				dir4 = dir3[0]
				return dir4
			else:
				return dir2
		else:
			if "(" in self.director:
				dir3 = self.director
				dir4 = dir3.split("(")
				dir5 = dir4[0]
				return dir6
			else:
				return self.director

	def get_writer(self):
		if "," in self.writer:
			wri0 = self.writer
			wri1 = wri0.split(",")
			wri2 = wri1[0]
			if "(" in wri2:
				wri3 = wri2.split("(")
				wri4 = wri3[0]
				return wri4
			else:
				return wri2
		else:
			if "(" in self.writer:
				wri3 = self.writer
				wri4 = wri3.split("(")
				wri5 = wri4[0]
				return wri5
			else:
				return self.writer

# Making instances of each getting_movie dict
my_movie_1 = Movie(getting_movie_1) 
my_movie_2 = Movie(getting_movie_2)
my_movie_3 = Movie(getting_movie_3)


# GETTING STRINGS OF ALL PRINCIPLE DIRECTOR AND WRITER'S NAMES

movie_director_1 = my_movie_1.get_director()
movie_writer_1 = my_movie_1.get_writer()

movie_director_2 = my_movie_2.get_director()
movie_writer_2 = my_movie_2.get_writer()

movie_director_3 = my_movie_3.get_director()
movie_writer_3 = my_movie_3.get_writer()

#____________________________________________________________________________________________________

# TASK 5: PULLING SUGGESTIONS FROM WIKIPEDIA

def get_wiki_suggs(input_q):

    # IF INPUTTED SEARCH QUERY IS CACHED
	if input_q in CACHE_DICTION2:
		#print("\nGetting Wikipedia suggestions from cached data...")

		# GETTING WIKI SUGGESTIONS FROM CACHE DICTIONARY
		wiki_dict = CACHE_DICTION2[input_q]

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

	# IF INPUTTED SEARCH QUERY IS NOT CACHED --- PULLING FROM WEB

	else:
		#print("\nRetrieving Wikipedia suggestions from web...")
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
		CACHE_DICTION2[input_q] = wiki_dict

	cached_suggs = open(CACHE_FNAME, 'w')
	cached_suggs.write(json.dumps(CACHE_DICTION2))
	cached_suggs.close()

	# RETURNING DICTIONARY OF SUGGESTIONS
	return wiki_dict

#____________________________________________________________________________________________________

# TASK 5: DEFINING FUNCTION GET_WIKI TO INVOKE GET_WIKI_SUGGS FUNCTION IF PROPER MOVIE INFO WAS ENTERED

def get_wiki(person):
	try:
		person_info = get_wiki_suggs(person)
		return person_info
	except:
		# TO PREVENT DISAMBIGUOUS ERRORS
		print("\n\nOops! We don't seem to have the director and writer of that movie in our database. Please try again with another movie.\n")
		sys.exit()

# TASK 6: INVOKING GET_WIKI FUNCTION ON THE DIRECTOR AND WRITER NAMES

director_wiki_1 = get_wiki(movie_director_1)
writer_wiki_1 = get_wiki(movie_writer_1)

director_wiki_2 = get_wiki(movie_director_2)
writer_wiki_2 = get_wiki(movie_writer_2)

director_wiki_3 = get_wiki(movie_director_3)
writer_wiki_3 = get_wiki(movie_writer_3)

#____________________________________________________________________________________________________

# TASK 7: CREATING CLASS WIKIPAGE

class Wikipage(object):
	def __init__(self, dict1):
		self.summary = dict1["summary"]
		self.categories = dict1["categories"]
		self.links = dict1["links"]
		self.sections = dict1["sections"]
		self.content = dict1["content"]

	def printable_list(self):
		print("\nBackground information:  \n" + self.summary)

		counter1 = 0
		print("\nSimilar pages: ")
		for link in self.links[:6]:
			counter1 += 1
			print(str(counter1) + ". " + link)
		print("\nCategories: ")

		counter2 = 0
		for category in self.categories[:6]:
			counter2 += 1
			print(str(counter2) + ". " + category)
		print("\n")

	def getting_all_content(self):
		a = "Background Information: "
		b = self.summary

		c = "Complete Wikipedia Page: "
		d = self.content

		print(a+b+c+d)

	def sections(self):
		if len(self.sections) > 0:
			return(sections)

#____________________________________________________________________________________________________

# TASK 8: CREATING CLASS WIKIPAGE INSTANCES: ONE FOR EACH PRINCIPLE DIRECTOR AND ONE FOR EACH PRINCIPLE WRITER

director_instance_1 = Wikipage(director_wiki_1)
writer_instance_1 = Wikipage(writer_wiki_1)

director_instance_2 = Wikipage(director_wiki_2)
writer_instance_2 = Wikipage(writer_wiki_2)

director_instance_3 = Wikipage(director_wiki_3)
writer_instance_3 = Wikipage(writer_wiki_3)

separator = " - - - - - - - - - - - - - - - - - - - - - - - - "

#print("\n" + separator + "\n\nMOVIE DIRECTOR: " + movie_director)
#director_instance.printable_list()

#print(separator + "\n\nMOVIE WRITER: " + movie_writer)
#writer_instance.printable_list()

#_____________________________________________________________________________________________________

# TASK 9: SETTING UP DATABASE FILE AND TABLES

conn = sqlite3.connect('si206finalproject.db')
cur = conn.cursor()

# TABLE 1 MOVIES
cur.execute("DROP TABLE IF EXISTS Movies")
statement1 = "CREATE TABLE IF NOT EXISTS "
statement1 += 'Movies (movie_title TEXT PRIMARY KEY, director TEXT, writer TEXT, plot TEXT, imdb_rating REAL)'

cur.execute(statement1)

# TABLE 2 DIRECTORS
cur.execute("DROP TABLE IF EXISTS Directors")
statement2 = "CREATE TABLE IF NOT EXISTS "
statement2 += 'Directors (movie_title TEXT PRIMARY KEY, summary TEXT, categories TEXT, links TEXT, sections TEXT, content TEXT)'

cur.execute(statement2)

# TABLE 3 WRITERS
cur.execute("DROP TABLE IF EXISTS Writers")
statement3 = "CREATE TABLE IF NOT EXISTS "
statement3 += 'Writers (movie_title TEXT PRIMARY KEY, summary TEXT, categories TEXT, links TEXT, sections TEXT, content TEXT)'

cur.execute(statement3)

#_____________________________________________________________________________________________________
# TASK 10: LOAD MOVIES AND WIKIS INTO DB






#_____________________________________________________________________________________________________
# TASK 11: COMPILE OUTPUT TEXT FILES FOR USER

# USE METHODS IN CLASS DEFINITIONS

#_____________________________________________________________________________________________________

# NEED TO REWRITE TEST CASES

#class SQL(unittest.TestCase):
#	def test_db_1(self):
#		conn = sqlite3.connect('si206finalproject.db')		
#		cur = conn.cursor()
#		cur.execute('SELECT * FROM Suggestions');
#		result = cur.fetchall()
#		self.assertTrue(len(result)>=10, "Testing that 10 strain suggestions were aggregated into the Suggestions table of the database")
#		conn.close()
#	def test_db_2(self):
#		conn = sqlite3.connect('si206finalproject.db')		
#		cur = conn.cursor()
#		cur.execute('SELECT * FROM Effects');
#		result = cur.fetchall()
#		self.assertTrue(len(result)>=10, "Testing that 10 strain suggestions were aggregated into the Effects table of the database")
#		conn.close()
#	def test_db_3(self):
#		conn = sqlite3.connect('si206finalproject.db')		
#		cur = conn.cursor()
#		cur.execute('SELECT * FROM Effects');
#		result = cur.fetchall()
#		self.assertTrue(len(result[1])==14, "Testing that 14 columns represent the 14 effect rankings")
#		conn.close()
#	def test_db_4(self):
#		conn = sqlite3.connect('si206finalproject.db')		
#		cur = conn.cursor()
#		cur.execute('SELECT * FROM Products');
#		result = cur.fetchall()
#		self.assertTrue(len(result)>=10, "Testing that 10 strain suggestions were aggregated into the Products database")
#		conn.close()

#unittest.main(verbosity=2)



