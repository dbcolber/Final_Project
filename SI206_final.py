# IMPORT STATEMENTS

# UNITTEST AND SYSTEM IMPORTS
import unittest
import sys

# GENERAL REQUEST / JSON IMPORTS
import requests
import json
import re

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
in1 = "Jaws"
getting_movie_1 = get_movies(in1)

in2 = "Alice in Wonderland"
getting_movie_2 = get_movies(in2)

in3 = "King Kong"
getting_movie_3 = get_movies(in3)

list_of_titles = [in1,in2,in3]

list_of_movie_dicts = [getting_movie_1, getting_movie_2, getting_movie_3]
#print(list_of_movie_dicts)

movie_dict = {}
for title in list_of_titles:
	movie_dict[title] = get_movies(title)

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
		self.runtime = getting_movie["runtime"]
		self.rated = getting_movie["rated"]

	def print_all_data(self):
		a = "Movie Title: {}\n".format(self.title)
		b = "Synopsis: {}\n".format(self.plot)
		c = "IMDB Rating: {}\n".format(self.rating)
		d = "Director: {}\n".format(self.director)
		e = "Writer: {}\n".format(self.writer)
		f = "Runtime: {}\n".format(self.runtime)
		g = "Rating: {}\n".format(self.rated)
		return a+b+c+d+e+f+g

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

movie_instance_list = [my_movie_1, my_movie_2, my_movie_3]

# GETTING STRINGS OF ALL PRINCIPLE DIRECTOR AND WRITER'S NAMES

#### ESTABLISH INDIVIDUAL VARIABLES TO USE FOR DB AGGREGATION

movie_director_1 = my_movie_1.get_director()
movie_writer_1 = my_movie_1.get_writer()

movie_director_2 = my_movie_2.get_director()
movie_writer_2 = my_movie_2.get_writer()

movie_director_3 = my_movie_3.get_director()
movie_writer_3 = my_movie_3.get_writer()

list_of_directors = [movie_director_1, movie_director_2, movie_director_3]
list_of_writers = [movie_writer_1, movie_writer_2, movie_writer_3]

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
		wiki_dict["images"] = wiki_page.images # a list of strings
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

# Use dictionary comprehension to create dicts of all directors' and writers' wikis to use for db

all_dir_data = {director: get_wiki(director) for director in list_of_directors}
all_wri_data = {writer: get_wiki(writer) for writer in list_of_writers}

#____________________________________________________________________________________________________

# TASK 7: CREATING CLASS WIKIPAGE

class Wikipage(object):
	def __init__(self, dict1):
		self.summary = dict1["summary"]
		self.categories = dict1["categories"]
		self.links = dict1["links"]
		self.images = dict1["images"]
		self.content = dict1["content"]

	def printable_list(self):
		return("\nBackground information:  \n" + self.summary)

		counter1 = 0
		return("\nSimilar pages: ")
		for link in self.links[:6]:
			counter1 += 1
			return(str(counter1) + ". " + link)
		return("\nCategories: ")

		counter2 = 0
		for category in self.categories[:6]:
			counter2 += 1
			return(str(counter2) + ". " + category)
		return("\n")

	def getting_all_content(self):

		c = "Complete Wikipedia Page: "
		d = self.content

		return(c+d)



#____________________________________________________________________________________________________

# TASK 8: CREATING CLASS WIKIPAGE INSTANCES: ONE FOR EACH PRINCIPLE DIRECTOR AND ONE FOR EACH PRINCIPLE WRITER

# Will be used for text file aggregation

director_instance_1 = Wikipage(director_wiki_1)
writer_instance_1 = Wikipage(writer_wiki_1)

director_instance_2 = Wikipage(director_wiki_2)
writer_instance_2 = Wikipage(writer_wiki_2)

director_instance_3 = Wikipage(director_wiki_3)
writer_instance_3 = Wikipage(writer_wiki_3)

director_instances_list = [director_instance_1, director_instance_2, director_instance_3]
writer_instances_list = [writer_instance_1, writer_instance_2, writer_instance_3]


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
statement1 += 'Movies (movie_title TEXT PRIMARY KEY, director TEXT, writer TEXT, plot TEXT, imdb_rating REAL, runtime REAL, rated TEXT)'

cur.execute(statement1)

# TABLE 2 DIRECTORS
cur.execute("DROP TABLE IF EXISTS Directors")
statement2 = "CREATE TABLE IF NOT EXISTS "
statement2 += 'Directors (director TEXT PRIMARY KEY, summary TEXT, categories TEXT, links TEXT, images TEXT, content TEXT)'

cur.execute(statement2)

# TABLE 3 WRITERS
cur.execute("DROP TABLE IF EXISTS Writers")
statement3 = "CREATE TABLE IF NOT EXISTS "
statement3 += 'Writers (writer TEXT PRIMARY KEY, summary TEXT, categories TEXT, links TEXT, images TEXT, content TEXT)'

cur.execute(statement3)

#_____________________________________________________________________________________________________
# TASK 10: LOAD MOVIES AND WIKIS INTO DB

# DB 1 - LOADING MOVIE DATA

for movie in movie_dict:
	insert_movie_info = "INSERT INTO Movies VALUES (?,?,?,?,?,?,?)"
	movie_66 = movie_dict[movie]
	movie_stuff = (movie, movie_66['director'], movie_66['writer'], movie_66['plot'], float(movie_66['imdb_rating']), movie_66['runtime'], str(movie_66['rated']))
	cur.execute(insert_movie_info, movie_stuff)

# DB 2 - LOAD DIRECTOR DATA

for director in all_dir_data:
	insert_dir_info = "INSERT INTO Directors VALUES (?,?,?,?,?,?)"
	dir_66 = all_dir_data[director]
	dir_stuff = (director, str(dir_66['summary']), str(dir_66['categories']), str(dir_66['links']), str(dir_66['images']), str(dir_66['content']))
	cur.execute(insert_dir_info, dir_stuff)

# DB 3 - LOAD WRITER DATA

for writer in all_wri_data:
	insert_wri_info = "INSERT INTO Writers VALUES (?,?,?,?,?,?)"
	wri_66 = all_wri_data[writer]
	wri_stuff = (writer, str(wri_66['summary']), str(wri_66['categories']), str(wri_66['links']), str(wri_66['images']), str(wri_66['content']))
	cur.execute(insert_wri_info, wri_stuff)

conn.commit()

#_____________________________________________________________________________________________________
# TASK 11: MAKE QUERIES TO DB

# QUERY 1 - EXTRACTING DIRECTORS WHOSE MOVIES HAVE A RATING OF 7 OR HIGHER 
query1 = 'SELECT Directors.director FROM Directors INNER JOIN Movies on Directors.director = Movies.director ORDER BY imdb_rating'
cur.execute(query1)
query1_object = cur.fetchall()

# QUERY 2 - GETTING ALL MOVIES THAT ARE PG
query2 = 'SELECT writer, LENGTH(content) FROM Writers ORDER BY LENGTH(content)'
cur.execute(query2)
query2_object = cur.fetchall()

# QUERY 3
query3 = 'SELECT Directors.director, Movies.runtime FROM Directors INNER JOIN Movies on Directors.director = Movies.director'
cur.execute(query3)
query3_object = cur.fetchall()

#_____________________________________________________________________________________________________
# TASK 12: COMPILE OUTPUT TEXT FILES FOR USER

# USE METHODS IN CLASS DEFINITIONS
 
txt_file = open('SI206_final_textfile.txt', 'w')
txt_file.write("\nMOVIE SUMMARIES\nA compilation of movie information, as well as biographies regarding the principle directors and writers\n\n")

new_movie_list = sorted(movie_instance_list, key = lambda x:x.rating, reverse = True)
#print(list(x.rating for x in new_movie_list))

all_movie_text = list(map(lambda x: x.print_all_data(), new_movie_list))
for item in all_movie_text:
	txt_file.write(item)
	txt_file.write("\n\n")

txt_file.write("===========================================================\n\nMOVIE DIRECTORS WIKI INFO (in order of highest rating movie rating) : \n")
# MOVIE DIRECTOR WIKI INFO

for director in director_instances_list:
	txt_file.write(str(director.printable_list()))
	txt_file.write(str(director.getting_all_content()))


txt_file.write("===========================================================\n\nMOVIE WRITERS WIKI INFO: \n\n")
# MOVIE WRITER WIKI INFO
for writer in writer_instances_list:
	txt_file.write(str(writer.printable_list()))
	txt_file.write(str(writer.getting_all_content()))

txt_file.write("\n\n===========================================================\n\nFUN FACTS ABOUT THE MOVIES, DIRECTORS, AND WRITERS!\n\n")
txt_file.write("Director with the best rated movie: " + str(query1_object[0]) + "\n")
txt_file.write("Writer with the longest Wikipedia page: " + str(query2_object[0]) + "\n")
txt_file.write("Director with the longest movie runtime: " + str(query3_object[0]) + "\n")


txt_file.close()

#_____________________________________________________________________________________________________

# TASK 13: TEST CASES
#class ClassTests(unittest.TestCase):
#	def test_movie_title(self):
#        movie1 = get_movies("Inside Out")
#        movie1_instance = Movie(movie1)
#        self.assertEqual(type(movie1_instance.title), string, "Testing that the instance's movie title is a string")
#    def test_class_director_method(self):
#        movie1 = get_movies("Inside Out")
#        movie1_instance = Movie(movie1)
#        self.assertEqual(type(movie1_instance.get_director()), string, "Testing that the method get_director returns a string")
#    def test_class_writer_method(self):
#        movie1 = get_movies("Inside Out")
#        movie1_instance = Movie(movie1)
#        self.assertEqual(type(movie1_instance.get_writer()), string, "Testing that the method get_writer returns a string")
#    def test_movie_str(self):
#        movie1 = get_movies("Inside Out")
#        movie1_instance = Movie(movie1)
#        self.assertEqual(type(movie1_instance.print_all_data(), string, "Testing that the method print_all_data returns a string")
#	def test_wiki(self):
#		 movie1 = get_movies("Inside Out")
#        movie1_instance = Movie(movie1)
#        movie1_dir = movie1_instance.get_director()
#        wiki1 = Wikipage(movie1_dir)
#        self.assertEqual(type(wiki1.printable_list()), string, "Testing that Wikipage method printable_list prints a str")

#class DbTests(unittest.TestCase):
#	def test_db_1(self):
#		conn = sqlite3.connect('si206finalproject.db')		
#		cur = conn.cursor()
#		cur.execute('SELECT * FROM Movies');
#		result = cur.fetchall()
#		self.assertTrue(len(result)>=3, "Testing that 3 movies were aggregated into the Movies table")
#		conn.close()
#	def test_db_2(self):
#		conn = sqlite3.connect('si206finalproject.db')		
#		cur = conn.cursor()
#		cur.execute('SELECT * FROM Directors');
#		result = cur.fetchall()
#		self.assertTrue(len(result)>=10, "Testing that 3 directors were aggregated into the Directors table of the database")
#		conn.close()
#	def test_db_3(self):
#		conn = sqlite3.connect('si206finalproject.db')		
#		cur = conn.cursor()
#		cur.execute('SELECT * FROM Writers');
#		result = cur.fetchall()
#		self.assertTrue(len(result[1])==14, "Testing that 3 writers in Writer DB")
#		conn.close()

#if __name__ == "__main__"
#	unittest.main(verbosity=2)



