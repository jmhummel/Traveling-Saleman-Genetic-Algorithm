#!/usr/bin/env python

import multiprocessing
import pickle
import random
import operator
import time
import sys
import itertools
import numpy
import math

import maputils

USE_STOCHASTIC_SELECT = True
USE_ELITISM = True

CAPITALS = maputils.CAPITALS
 
# cachedDistDur = pickle.load(open('cache.p', 'r'))

def getDistDur(origin, destination):
	xDistance = abs(origin[0] - destination[0])
	yDistance = abs(origin[1] - destination[1])
	return math.sqrt(xDistance**2 + yDistance**2)

NUM_POP = 100
# NUM_POP = 1000
NUM_SEEDS = NUM_POP
POOL_SIZE = multiprocessing.cpu_count()
# POOL_SIZE = 1
# NUM_CAPITALS = 9
NUM_CAPITALS = len(CAPITALS)

def init():
	seeds = []
	for i in xrange(NUM_SEEDS):
		r = range(NUM_CAPITALS)
		random.shuffle(r)
		seeds.append(r)
	return seeds

def deDup(route):
	route = tuple(route)
	idx = route.index(0)
	route = route[idx:] + route[:idx]
	if route[-1] < route[1]:
		return route[:1] + tuple(reversed(route[1:]))
	return route

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
		totalDur += getDistDur(point1, point2)
	# cachedRouteDur[route] = totalDur
	# print totalDur, route
	return totalDur

def normalize(durationMap):
	totalInvertedDuration = 0
	for route, duration in durationMap.iteritems():
		totalInvertedDuration += 1 / float(duration)
	fitnessMap = {}
	for route, duration in durationMap.iteritems():
		fitnessMap[route] = (1 / float(duration)) / totalInvertedDuration
	return fitnessMap

def calcAccumulatedFitness(fitnessMap):
	sortedFitnessList = sorted(fitnessMap.items(), key=operator.itemgetter(1), reverse=True)
	accumulatedFitnessList = []
	accumulated = 0.0
	for t in sortedFitnessList:
		accumulatedFitnessList.append((t[0], t[1] + accumulated))
		accumulated += t[1]
	return accumulatedFitnessList

# Fitness proportionate selection
def select(accumulatedFitnessMap):
	r = random.random()
	j = 0
	# print 'r', r
	for chromosome in accumulatedFitnessMap:
		if r < chromosome[1]:
			return chromosome[0]

# Stochastic acceptance selection 
def stochasticSelect(fitnessMap):
	maxFitness = max(fitnessMap.values())
	while True:
		chromosome = random.choice(fitnessMap.keys())
		r = random.random()
		if r < fitnessMap[chromosome] / float(maxFitness):
			return chromosome	

# Partially matched crossover
def crossover(mate1, mate2):
	# print mate1
	# print mate2
	r1 = random.randint(0, len(mate1))
	r2 = random.randint(0, len(mate1))
	point1 = min(r1, r2)
	point2 = max(r1, r2)

	offspring1 = list(mate2)
	for i in xrange(point1, point2):
		if offspring1[i] != mate1[i]:
			for j in xrange(len(offspring1)):
				if offspring1[j] == mate1[i]:
					offspring1[j] = offspring1[i]
					offspring1[i] = mate1[i]
	offspring2 = list(mate1)
	for i in xrange(point1, point2):
		if offspring2[i] != mate2[i]:
			for j in xrange(len(offspring2)):
				if offspring2[j] == mate2[i]:
					offspring2[j] = offspring2[i]
					offspring2[i] = mate2[i]
	# print point1, point2
	# print offspring
	return [offspring1, offspring2]

CROSSOVER_RATE = 0.7
# Ordered crossover
def orderedCrossover(mate1, mate2):
	# print mate1
	# print mate2
	start = random.randint(0, len(mate1))
	length = random.randint(0, len(mate1))
	
	mate1 = mate1[start:] + mate1[:start]
	mate2 = mate2[start:] + mate2[:start]

	s = set(mate1[:length])
	l = [x for x in mate2 if x not in s]
	offspring1 = list(mate1[:length]) + l

	s = set(mate2[:length])
	l = [x for x in mate1 if x not in s]
	offspring2 = list(mate2[:length]) + l

	return [offspring1, offspring2]

MUTATION_RATE = 0.015
def mutate(chromosome):
	for i in xrange(len(chromosome)-1):
		if random.random() <= MUTATION_RATE:
			j = random.randint(0, len(chromosome)-1)
			tmp = chromosome[i]
			chromosome[i] = chromosome[j]
			chromosome[j] = tmp

	# Reverse subsection
	if random.random() <= 0.2:
		start = random.randint(0, len(chromosome)-1)
		length = random.randint(4, len(chromosome)-4)
		chromosome = chromosome[start:] + chromosome[:start]
		chromosome = list(reversed(chromosome[:length])) + chromosome[length:]

ITERATIONS = 100000
# MAX_DURATION = 2500000
MAX_DURATION = 0

def ga():
	startTime = time.time()
	bestRoute = None
	bestDur = 0
	routes = init()
	stats = []
	loop = 0
	durationMap = {}
	routes = [ deDup(route) for route in routes ]
	for route in routes:
		durationMap[tuple(route)] = calcDuration(route)

	pool = multiprocessing.Pool(POOL_SIZE)

	while bestRoute is None or bestDur > MAX_DURATION:
		# routes = [ deDup(route) for route in routes ]
		
		# for route in routes:
		# 	durationMap[tuple(route)] = calcDuration(route)



		fitnessMap = normalize(durationMap)

		if (USE_STOCHASTIC_SELECT):
			accumulatedFitnessList = None
			shortestRoute = min(durationMap.items(), key=operator.itemgetter(1))[0]
		else:
			accumulatedFitnessList = calcAccumulatedFitness(fitnessMap)
			shortestRoute = accumulatedFitnessList[0][0]

		averageDuration = float(sum(durationMap.values())) / len(durationMap)
		
		if (bestRoute is None or durationMap[shortestRoute] < bestDur):
			bestRoute = shortestRoute
			bestDur = durationMap[shortestRoute]
			# stats.append(str(bestRoute) + ' ' + str(bestDur) + ' ' + str(averageDuration) + ' ' + str(loop) + ' ' + str(time.time() - startTime))
			stats.append(str(bestDur) + '\t' + str(bestRoute) + '\t' + str(averageDuration) + '\t' + str(loop) + '\t' + str(time.time() - startTime))
			print stats[-1]
		
		# print '\n'.join(stats)
		
		
		# args1 = [fitnessMap for i in xrange(NUM_POP / 2)]
		# args2 = [accumulatedFitnessList for i in xrange(NUM_POP / 2)]
		args = [(fitnessMap, accumulatedFitnessList) for i in xrange(NUM_POP / 2)]
		results = list(itertools.chain.from_iterable(pool.map(worker, args)))
		routes = [t[0] for t in results]
		durationMap = {t[0]:t[1] for t in results}

		if USE_ELITISM:
			routes.append(bestRoute)
			durationMap[bestRoute] = bestDur

		loop += 1
	# print '\n'.join(stats)
	# print stats[-1]
	# print [CAPITALS[i] for i in bestRoute]

	pool.close()
	pool.join()

	# print time.time() - startTime
	return time.time() - startTime

def worker(args):
	fitnessMap = args[0]
	accumulatedFitnessList = args[1]
	if (USE_STOCHASTIC_SELECT):
		mate1 = stochasticSelect(fitnessMap)
		mate2 = stochasticSelect(fitnessMap)
	else:
		mate1 = select(accumulatedFitnessList)
		mate2 = select(accumulatedFitnessList)
	offspring = orderedCrossover(mate1, mate2)
	offspring1 = offspring[0]
	offspring2 = offspring[1]
	mutate(offspring1)
	mutate(offspring2)
	return ((deDup(offspring1), calcDuration(offspring1)), (deDup(offspring2), calcDuration(offspring2)))

NUMBER_OF_TESTS = 20
def test():
	totalTime = 0
	testResults = [ga() for i in xrange(NUMBER_OF_TESTS)]
	print 'For', NUMBER_OF_TESTS, 'tests:'
	print 'mean:', numpy.mean(testResults)
	print 'std:', numpy.std(testResults)

#test()
ga() 