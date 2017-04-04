#!/usr/bin/env python

import requests
import pickle

import maputils

API_KEY = maputils.config['api_keys']['google_distance_matrix']
BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix'
CAPITALS = maputils.CAPITALS

# cachedDistDur = pickle.load(open('cache.p', 'rb'))
cachedDistDur = {}

def getDistDur(origin, destination):
	# print origin, destination
	key = tuple(sorted([origin, destination]))
	if key in cachedDistDur:
		# print origin, destination, 'from cache'
		return cachedDistDur[key]
	origin = origin.replace(' ','+')
	destination = destination.replace(' ','+')
	r = requests.get(BASE_URL + '/json?units=imperial&origins=' + origin + '&destinations=' + destination + '&key=' + API_KEY)
	if r.json()['status'] == 'OK':
		dist = r.json()['rows'][0]['elements'][0]['distance']['value']
		time = r.json()['rows'][0]['elements'][0]['duration']['value']
		result = (dist, time)
		cachedDistDur[key] = result
		print key, result
		# print origin, destination, result
		return result
	else:
		raise Exception('Over api limit!')

for p1 in CAPITALS[:50]:
	print p1
	for p2 in CAPITALS[:50]:
		if p1 != p2:
			getDistDur(p1, p2)

pickle.dump(cachedDistDur, open('cache.p', 'wb'), -1)