import pickle
import math
import polyline
import yaml
import random

geoCache        = pickle.load(open('geoCache.p', 'rb'))
directionsCache = pickle.load(open('directions.p','rb'))
config          = yaml.load(open("config.yml", 'r'))

def getCoords(place):
	return geoCache[place]

def getCoordString(place):
	return str(geoCache[place][0]) + ',' + str(geoCache[place][1])

def getDirections(origin, destination):
	return directionsCache[(origin, destination)]

def roughDist(point1, point2):
	return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def perpendicularDistance(point, lineStart, lineEnd):
	numerator = math.fabs( (lineEnd[0]-lineStart[0])*point[1] - (lineEnd[1]-lineStart[1])*point[0] + lineEnd[1]*lineStart[0] - lineEnd[0]*lineStart[1] )
	denominator = math.sqrt( (lineEnd[0]-lineStart[0])**2 + (lineEnd[1]-lineStart[1])**2 )
	return numerator / denominator

def DouglasPeucker(pointList, epsilon):
    # Find the point with the maximum distance
    dmax = 0
    index = 0
    end = len(pointList)
    for i in xrange(1, end-1):
        d = perpendicularDistance(pointList[i], pointList[0], pointList[-1]) 
        if d > dmax:
            index = i
            dmax = d
    # If max distance is greater than epsilon, recursively simplify
    if dmax > epsilon:
        # Recursive call
        recResults1 = DouglasPeucker(pointList[:index+1], epsilon)
        recResults2 = DouglasPeucker(pointList[index:], epsilon)

        # Build the result list
        resultList = recResults1[:-1] + recResults2
    else:
        resultList = [pointList[0], pointList[-1]]
    # Return the result
    return resultList

def getPoly(route, epsilon):
	route = [ CAPITALS[i] for i in route ]
	legs = zip(route, route[1:] + route[:1])
	coordinates = []
	for leg in legs:
		legCoords = DouglasPeucker(getDirections(*leg), epsilon)
		if leg == legs[-1]:
			coordinates += legCoords
		else:
			coordinates += legCoords[:-1]
	return polyline.encode(coordinates)

def mapUrl(poly):
	BASE_URL = 'https://maps.googleapis.com/maps/api/staticmap?size=640x640&scale=2'
	API_KEY = config['api_keys']['google_static_maps']
	url = BASE_URL
	iconUrl = 'http://i.imgur.com/n84gQUv.png'
	# iconUrl = 'http://i.imgur.com/cyy5Me4.png'
	url += '&markers=shadow:false|icon:' + iconUrl
	for city in CAPITALS:
		url += '|' + getCoordString(city)
	url += '&path=color:0x0000ffaa|weight:2|enc:' + poly + '&key=' + API_KEY
	return url

def drawLeg(place1, place2, m):
	location1 = getCoords(place1)
	location2 = getCoords(place2)

	m.drawgreatcircle(location1[1], location1[0], location2[1], location2[0], color='#0000ff80')

def drawRoute(route, plt):
	list1 = route
	list2 = route[1:] + route[:1]
	legs = zip(list1, list2)
	for leg in legs:
		place1 = CAPITALS[leg[0]]
		place2 = CAPITALS[leg[1]]
		plt.plot([place1[0], place2[0]], [place1[1],place2[1]], color='r', marker = 'o')

# CAPITALS = [
# 	(60, 200),
# 	(180, 200),
# 	(80, 180),
# 	(140, 180),
# 	(20, 160),
# 	(100, 160),
# 	(200, 160),
# 	(140, 140),
# 	(40, 120),
# 	(100, 120),
# 	(180, 100),
# 	(60, 80),
# 	(120, 80),
# 	(180, 60),
# 	(20, 40),
# 	(100, 40),
# 	(200, 40),
# 	(20, 20),
# 	(60, 20),
# 	(160, 20)
# ]

CAPITALS = [(random.randint(1,200), random.randint(1,200)) for i in xrange(8)]