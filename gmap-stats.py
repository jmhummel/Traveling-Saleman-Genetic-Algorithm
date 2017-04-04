import polyline
import requests
import pickle
import shutil
import csv
import math

import maputils

csvfile = open('stats.tsv', 'rb')
stats = csv.reader(csvfile, delimiter='\t')
routes = [ list(eval(row[1])) for row in stats ]

for i in xrange(len(routes)):
# for i in xrange(len(routes)-1,len(routes)):

	filename = 'pics/' + '{:03}'.format(i) + '.png'
	# route = routes[i]
	route = routes[i]

	poly = maputils.getPoly(route, 0.15)
	url = maputils.mapUrl(poly)

	r = requests.get(url, stream=True)
	if r.status_code == 200:
	    with open(filename, 'wb') as f:
	        r.raw.decode_content = True
	        shutil.copyfileobj(r.raw, f) 
	        print len(url), len(url) - len(poly), len(poly), len(poly)/float(len(polyline.decode(poly))), filename #, routes[i]
	else:
		print len(url), len(url) - len(poly), len(poly), len(poly)/float(len(polyline.decode(poly))), r.status_code, 'ERROR'
		break

