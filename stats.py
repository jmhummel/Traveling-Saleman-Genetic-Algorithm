import matplotlib.pyplot as plt
import pickle
import csv

import maputils

csvfile = open('stats.tsv', 'rb')
stats = csv.reader(csvfile, delimiter='\t')
routes = [ tuple(eval(row[1])) for row in stats ]

for i in xrange(len(routes)):
	plt.clf()
	maputils.drawRoute(routes[i], plt)
	filename = '{:03}'.format(i) + '.png'
	plt.savefig('pics/' + filename, dpi=300, bbox_inches='tight')
	print filename, routes[i]