import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pickle

# create the figure and axes instances.
fig = plt.figure()
ax = fig.add_axes([0.1,0.1,0.8,0.8])
# setup of basemap ('lcc' = lambert conformal conic).
# use major and minor sphere radii from WGS84 ellipsoid.
m = Basemap(llcrnrlon=-145.5,llcrnrlat=1.,urcrnrlon=-2.566,urcrnrlat=46.352,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',area_thresh=1000.,projection='lcc',\
            lat_1=50.,lon_0=-107.,ax=ax)

# draw coastlines and political boundaries.
m.drawcoastlines()
m.drawcountries()
m.drawstates()

pickle.dump(m,open('map.p','wb'),-1)