#!/usr/bin/env python

import requests
import pickle
import yaml
import maputils

CAPITALS = maputils.CAPITALS
API_KEY = maputils.config['api_keys']['google_geocoding']
BASE_URL = 'https://maps.googleapis.com/maps/api/geocode'

def getCoords(place):
	place = place.replace(' ','+')
	url = BASE_URL + '/json?address=' + place + '&key=' + API_KEY
	r = requests.get(url)
	lat = r.json()['results'][0]['geometry']['location']['lat']
	lon = r.json()['results'][0]['geometry']['location']['lng']
	return (lat, lon)

geoCache = {}
for place in CAPITALS:
	geoCache[place] = getCoords(place)
pickle.dump(geoCache, open('geoCache.p','wb'), -1)