from graph import *
from numpy import random
import numpy as np
import random


class GraphGenerator:
	def getEdgeWeight(lo, hi, centre, deviation, trivialProbability):
		probability = random.uniform(0,1)
		if probability <= trivialProbability:
			weight = random.uniform(lo, hi)
			return (weight, weight, weight)
		left, right = centre, centre
		length = (hi - lo) * deviation
		left = max(lo, left - length)
		right = min(hi, left + length)
		weight = random.uniform(left right)
		return (lo, hi, weight)

	def costructGraph(self, n, m, lo, hi, centre = None, deviation = 0.5, trivialProbability = 0.5):
		if centre == None:
			centre = (lo + hi) / 2
		if n > 1000 or m < n-1 or m > n*(n - 1)//2:
			assert False
		if lo < 0 or hi < lo:
			assert False
		if centre < lo or centre > hi:
			assert False
		if deviation < 0 or deviation > 1:
			assert False
		if trivialProbability < 0 or trivialProbability > 1:
			assert False
		order = [i for i in range(1, n + 1)]
		order = np.array(order)
		random.shuffle(order)
		order = order.tolist()
		parent = [-1 for i in range(n + 1)]
		edgeSet = set()
		for i in range(1, n):
			parent[order[i]] = order[random.randint(0, i-1)]
		edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual = [], [], [], [], []
		for i in range(1, n):
			edgeFrom.append(order[i])
			edgeTo.append(parent[order[i]])
			edgeSet.add((order[i], parent[order[i]]))
			edgeSet.add((parent[order[i]], order[i]))
			weights = getEdgeWeight(lo, hi, centre, deviation, trivialProbability)
			edgeLo.append(weights[0])
			edgeHi.append(weights[1])
			edgeActual.append(weights[2])
		m -= (n - 1)
		for i in range(m):
			u, v = random.randint(1, n), random.randint(1, n)
			while u == v or (u, v) in edgeSet:
				v = random.randint(1, n)
			edgeFrom.append(u)
			edgeTo.append(v)
			edgeSet.add((u, v))
			edgeSet.add((v, u))
			weights = getEdgeWeight(lo, hi, centre, deviation, trivialProbability)
			edgeLo.append(weights[0])
			edgeHi.append(weights[1])
			edgeActual.append(weights[2])
		graph = UncertainGraph()
		graph.buildFromParameters(edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual)
		return graph

	# All the edges are trivial
	def edgeCaseA(n, m, weight):
		if n > 1000 or m < n-1 or m > n*(n - 1)//2:
			assert False
		if weight < 0:
			assert False
		order = [i for i in range(1, n + 1)]
		order = np.array(order)
		random.shuffle(order)
		order = order.tolist()
		parent = [-1 for i in range(n + 1)]
		for i in range(1, n):
			parent[order[i]] = order[random.randint(0, i-1)]
		edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual = [], [], [], [], []
		for i in range(1, n):
			edgeFrom.append(order[i])
			edgeTo.append(parent[order[i]])
			edgeSet.add((order[i], parent[order[i]]))
			edgeSet.add((parent[order[i]], order[i]))
			edgeLo.append(weight)
			edgeHi.append(weight)
			edgeActual.append(weight)
		m -= (n - 1)
		for i in range(m):
			u, v = random.randint(1, n), random.randint(1, n)
			while u == v or (u, v) in edgeSet:
				v = random.randint(1, n)
			edgeFrom.append(u)
			edgeTo.append(v)
			edgeSet.add((u, v))
			edgeSet.add((v, u))
			edgeLo.append(weight)
			edgeHi.append(weight)
			edgeActual.append(weight)
		graph = UncertainGraph()
		graph.buildFromParameters(edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual)
		return graph

	# All the edges are either lo or hi
	def edgeCaseB(n, m, lo, hi):
		if n > 1000 or m < n-1 or m > n*(n - 1)//2:
			assert False
		if lo < 0 or hi < lo:
			assert False
		order = [i for i in range(1, n + 1)]
		order = np.array(order)
		random.shuffle(order)
		order = order.tolist()
		parent = [-1 for i in range(n + 1)]
		edgeSet = set()
		for i in range(1, n):
			parent[order[i]] = order[random.randint(0, i-1)]
		edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual = [], [], [], [], []
		for i in range(1, n):
			edgeFrom.append(order[i])
			edgeTo.append(parent[order[i]])
			edgeSet.add((order[i], parent[order[i]]))
			edgeSet.add((parent[order[i]], order[i]))
			edgeLo.append(lo)
			edgeHi.append(hi)
			weight = lo
			if random.randint(0,1):
				weight = hi
			edgeActual.append(weight)
		m -= (n - 1)
		for i in range(m):
			u, v = random.randint(1, n), random.randint(1, n)
			while u == v or (u, v) in edgeSet:
				v = random.randint(1, n)
			edgeFrom.append(u)
			edgeTo.append(v)
			edgeSet.add((u, v))
			edgeSet.add((v, u))
			edgeLo.append(lo)
			edgeHi.append(hi)
			weight = lo
			if random.randint(0,1):
				weight = hi
			edgeActual.append(weight)
		graph = UncertainGraph()
		graph.buildFromParameters(edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual)
		return graph

	# Complete Graph
	def edgeCaseB(n, lo, hi, centre = None, deviation = 0.5, trivialProbability = 0.5):
		return self.costructGraph(n, n*(n-1)//2, lo, hi, centre, deviation, trivialProbability)

	