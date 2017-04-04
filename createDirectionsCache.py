#!/usr/bin/env python

import requests
import pickle
import polyline

import maputils

API_KEY = maputils.config['api_keys']['google_directions']
BASE_URL = 'https://maps.googleapis.com/maps/api/directions/json?'
CAPITALS = maputils.CAPITALS

# directionsCache = pickle.load(open('directions.p','rb'))
directionsCache = {}

def getDirections(origin, destination):
	if (origin, destination) in directionsCache:
		directions = directionsCache[(origin, destination)]
		# print origin, destination
	else:
		url = BASE_URL + 'origin=' + origin + '&destination=' + destination + '&key=' + API_KEY
		print origin, destination, '\t' + url
		r = requests.get(url)
		# print url
		if r.json()['status'] == 'OK':
			poly = r.json()['routes'][0]['overview_polyline']['points']
			directions = polyline.decode(poly)
		else:
			print r.json()
			raise Exception('Something went wrong')
		directionsCache[(origin, destination)] = directions
		directionsCache[(destination, origin)] = list(reversed(directions))
	return directions

for p1 in CAPITALS[:50]:
	# print p1
	for p2 in CAPITALS[:50]:
		if p1 != p2:
			getDirections(p1, p2)

pickle.dump(directionsCache, open('directions.p','wb'), -1)