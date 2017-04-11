import unittest
import itertools
import collections

import requests
import requests.auth
import json

import yelp
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from pprint import pprint

import sqlite3

#____________________________________________________________________________________________________

# Pulling data from Cannabis Reports API

cr_api_key = "c1150560c584de130b1ecdec7f9d3a7f1298ab8d"
#cr_base_url = "https://www.cannabisreports.com/api/v1.0/strains/search/:query"

user_inp = input("Enter a medical symptom:  ")

br = "https://www.cannabisreports.com/api/v1.0/strains/search/" + user_inp
resp = requests.get(br, params = {'X-API-Key':cr_api_key})

resp_dict = json.loads(resp.text)

for item in resp_dict["data"]:
	print(item['name'])
