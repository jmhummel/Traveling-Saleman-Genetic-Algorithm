#!/usr/bin/env python

import multiprocessing
import pickle
import random
import operator
import time
import sys
import itertools

import maputils

USE_STOCHASTIC_SELECT = True
USE_ELITISM = True

CAPITALS = maputils.CAPITALS
 
cachedDistDur = pickle.load(open('cache.p', 'r'))

def getDistDur(origin, destination):
	# print origin, destination
	key = tuple(sorted([origin, destination]))
	if key in cachedDistDur:
		# print origin, destination, 'from cache'
		return cachedDistDur[key]
	else:
		raise Exception('Not found in cache') 

# NUM_POP = 100
NUM_POP = 1000
NUM_SEEDS = NUM_POP
POOL_SIZE = multiprocessing.cpu_count()
# POOL_SIZE = 1
NUM_CAPITALS = 9

def deDup(route):
	route = tuple(route)
	idx = route.index(0)
	route = route[idx:] + route[:idx]
	if route[-1] < route[1]:
		return route[:1] + tuple(reversed(route[1:]))
	return route

def isDeDuped(route):
	return route[1] < route[-1]

def calcDuration(route):
	route = tuple(route)
	# if route in cachedRouteDur:
	# 	print cachedRouteDur[route], route, 'cached'
	# 	return cachedRouteDur[route]
	list1 = route
	list2 = route[1:] + route[:1]
	legs = zip(list1, list2)
	totalDur = 0
	for leg in legs:
		point1 = CAPITALS[leg[0]]
		point2 = CAPITALS[leg[1]]
		totalDur += getDistDur(point1, point2)[1]
	# cachedRouteDur[route] = totalDur
	# print totalDur, route
	return totalDur


ITERATIONS = 100000
# MAX_DURATION = 600000
MAX_DURATION = 0

def ga():
	startTime = time.time()
	bestRoute = multiprocessing.Array('i', [0]*NUM_CAPITALS)
	bestDur = multiprocessing.Value('d', 0.0)

	stats = []
	loop = 0

	pool = multiprocessing.Pool(POOL_SIZE)
	lock = multiprocessing.Lock()

	s = set(range(1, NUM_CAPITALS))
	for i in xrange(1, NUM_CAPITALS):
		for j in xrange(i+1, NUM_CAPITALS):
			for route in itertools.permutations(s - set([i, j])):
				route = (0,i) + route + (j,)
				multiprocessing.Process(target=worker, args=(lock, route, loop, bestRoute, bestDur, startTime)).start()
				loop += 1

	# for route in itertools.permutations(range(1, NUM_CAPITALS)):
	# 	route = (0,) + route
	# 	multiprocessing.Process(target=worker, args=(lock, route, loop, bestRoute, bestDur, startTime)).start()
	# 	loop += 1
		
	# print '\n'.join(stats)
	# print stats[-1]
	# print [CAPITALS[i] for i in bestRoute]
	return time.time() - startTime
	# pool.close()
	# pool.join()

def worker(lock, route, loop, bestRoute, bestDur, startTime):
	# route = tuple(route)
	# if not isDeDuped(route):
	# 	return
	duration = calcDuration(route)

	lock.acquire()
	if (bestRoute[:] == [0]*NUM_CAPITALS or duration < bestDur.value):
		for i, v in enumerate(route):
			bestRoute[i] = v
		bestDur.value = duration
		stats = []
		stats.append(str(duration) + '\t' + str(route) + '\t' + str(loop) + '\t' + str(time.time() - startTime))
		print stats[-1]
	lock.release()

NUMBER_OF_TESTS = 20
def test():
	totalTime = 0
	for i in xrange(NUMBER_OF_TESTS):
		totalTime += ga()
	print totalTime / NUMBER_OF_TESTS

#test()
ga() 