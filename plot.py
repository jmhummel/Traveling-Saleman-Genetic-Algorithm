import matplotlib.pyplot as plt
import pickle
import csv

import maputils

csvfile = open('stats.tsv', 'rb')
stats = csv.reader(csvfile, delimiter='\t')
route = tuple(eval(list(stats)[-1][1]))

m = pickle.load(open('map.p','rb'))
maputils.drawRoute(route, m)

plt.show()