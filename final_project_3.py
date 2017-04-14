# IMPORT STATEMENTS

import unittest

import requests
import json

import wikipedia

from pprint import pprint

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

# PULLING SUGGESTIONS FROM WIKIPEDIA

def get_wiki_suggs(input_q):

    # IF INPUTTED SEARCH QUERY IS CACHED
	if input_q in CACHE_DICTION:
		print("Getting Wikipedia suggestions from cached data...")

		# GETTING WIKI SUGGESTIONS FROM CACHE DICTIONARY
		wiki_suggs = CACHE_DICTION[input_q]

	# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

	# IF INPUTTED SEARCH QUERY IS NOT CACHED --- PULLING FROM WEB

	else:
		print("Retrieving Wikipedia suggestions from web...")

		# GETTING WIKI SUGGESTIONS
		wiki_suggs = wikipedia.search(input_q)

		# CACHING LIST OF SUGGESTIONS
		CACHE_DICTION[input_q] = wiki_suggs

	cached_suggs = open(CACHE_FNAME, 'w')
	cached_suggs.write(json.dumps(CACHE_DICTION))
	cached_suggs.close()

	# RETURNING DICTIONARY OF SUGGESTIONS
	return wiki_suggs

#____________________________________________________________________________________________________

# ASKING USER FOR SEARCH TERM AND INVOKING IT ON get_wiki_suggs FUNCTION
while True:
	try:
		user_input = input("\nWelcome to your personal encyclopedia. Please enter a specific search term: \n")
		user_suggs = get_wiki_suggs(user_input)
		break
	except:
		# TO PREVENT DISAMBIGUOUS ERRORS
		print("\n\nOops! Your Search term was too broad. Please be more specific and try again: ")

count = 0
for item in user_suggs[:3]:
	count += 1
	print("\n" + str(count) + ". " + item)
	wiki = wikipedia.WikipediaPage(item)
	print(wiki.summary)

#_____________________________________________________________________________________________________

# PULL WIKIPEDIA INFORMATION FOR EACH STRAIN















