import polyline
import requests
import csv
import pickle
import shutil
from subprocess import call

import maputils

csvfile = open('stats.tsv', 'rb')
stats = csv.reader(csvfile, delimiter='\t')
route = list(eval(list(stats)[-1][1]))

poly = maputils.getPoly(route, 0.2)
url = maputils.mapUrl(poly)

filename = 'goog.png'
r = requests.get(url, stream=True)
if r.status_code == 200:
    with open(filename, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f) 
        call(["open", filename])
else:
	print r.status_code, 'Error'