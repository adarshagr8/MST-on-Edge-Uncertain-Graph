from graph import *
from bipartite_weighted import *
from functools import cmp_to_key
from copy import deepcopy
from checker import *

def compareEdges(e, f):
	if e.lower != f.lower:
		return e.lower - f.lower
	elif e.upper != f.lower:
		return e.upper - f.upper
	else:
		return 0


def weightedOptimalQuerySet(g):
	"""Generates an optimal query set for the given uncertain graph."""
	# PHASE 1
	# Sort edges according to the comparator above and add them to an empty forest in the sorted order.
	sortedEdges = []
	for e in g.edges:
		sortedEdges.append(e)

	sortedEdges = sorted(sortedEdges, key = cmp_to_key(compareEdges))
	common = []
	choices = []
	curgraph = DynamicForest(g.size)
	while len(sortedEdges):
		e = sortedEdges[0]
		sortedEdges.pop(0)
		# If no cycle is introduced, add and continue
		if not curgraph.cycleCheck(e):
			curgraph.addEdge(e)
			continue
		# Find all edges in the cycle introduced by the newly added edge
		cycle = curgraph.getCycle(e)
		# sanity check for cycle
		assert len(cycle) > 1
		# if len(cycle) <= 1:
		# 	print(cycle)
		curgraph.addEdge(e)
		# check case (a): cycle has an always maximal edge
		hasMaximal = True
		# Find the edge with maximum upper limit. This is our candidate for the always maximal edge.
		candidate = cycle[0]
		for e in cycle:
			if e.upper > candidate.upper:
				candidate = e

		# Check if the candidate is always maximal.
		for e in cycle:
			if e.upper > candidate.lower:
				hasMaximal = False

		if hasMaximal:
			# case (a) is satisfied: remove the always maximal edge and continue
			curgraph.removeEdge(candidate)
			continue

		# check case (b): there exists an edge in the cycle whose update must be in any update solution
		flag = False
		# If there is an edge with its actual weight more than the candidate's, then candidate must be queried in any update solution.
		for e in cycle:
			if e.actual > candidate.actual:
				flag = True
				break

		# If candidate has maximal actual weight and there is an edge with its upper limit higher than the candidate's actual weight
		# then that edge must be queried in any update solution.
		if not flag:
			for e in cycle:
				if e.upper > candidate.actual and e != candidate:
					flag = True
					candidate = e
					break

		# If candidate has maximal actual weight and there is an edge with its actual weight more than the candidate's lower limit
		# then the candidate must be queried in any update solution.
		if not flag:
			for e in cycle:
				if e.actual > candidate.lower and e != candidate:
					flag = True
					break

		if flag:
			# case (b) satisfied: update candidate, remove from curgraph and add to common and back to sortedEdges
			curgraph.removeEdge(candidate)
			common.append(candidate)
			updatedCandidate = deepcopy(candidate)
			updatedCandidate.query()
			sortedEdges.append(updatedCandidate)
			sortedEdges = sorted(sortedEdges, key = cmp_to_key(compareEdges))
			continue
		# check case (c): there is a choice of updates that establishes an edge as an always maximal edge in the cycle C
		# either query the candidate or all edges in the cycle with their upper limit higher than the candidate's lower limit.
		B = []
		for e in cycle:
			if e != candidate and e.upper > candidate.lower:
				B.append(e)
		choices.append((candidate, B))

		maximalEdge = cycle[0]
		for e in cycle:
			if e.actual > maximalEdge.actual:
				maximalEdge = e
		curgraph.removeEdge(maximalEdge)


	# PHASE 2
	# remove edges present in common from the edges in choices
	newchoices = []
	for d, B in choices:
		assert d not in common
		newB = []
		for e in B:
			if e not in common:
				newB.append(e)
		if len(newB) > 0:
			newchoices.append((d, newB))

	choices = newchoices
	
	
	# PHASE 3
	# In the choices, the sets L = {d: (d, B) belongs to choices} and R = union of all Bs are disjoint.
	# Minimum vertex cover in the graph formed by the set of edges
	# {(d, b) : there exists a (d, B) belonging to choices s.t. b belongs to B} corresponds to an optimal query set. 
	# Left side of the bipartite graph corresponds to L and right to R.
	# Number the left vertices
	leftWeights = []
	rightWeights = []
	leftEdgeToIndex = {}
	leftEdges = []
	for d, B in choices:
		leftEdgeToIndex[d] = len(leftEdges)
		leftEdges.append(d)
		leftWeights.append(d.cost)

	# Generate the union of all Bs s.t. (d, B) belongs to choices
	choiceUnion = set()
	for d, B in choices:
		for e in B:
			choiceUnion.add(e)

	# Number the right vertices
	rightEdges = list(choiceUnion)
	rightEdgeToIndex = {}
	for e in rightEdges:
		rightEdgeToIndex[e] = len(rightEdgeToIndex)
		rightWeights.append(e.cost)


	edgesInGprime = []
	for d, B in choices:
		for e in B:
			edgesInGprime.append((leftEdgeToIndex[d], rightEdgeToIndex[e]))

	# Find minimum vertex cover and recover solution from it and return


	graph = WeightedBipartiteGraph(edgesInGprime, leftWeights, rightWeights)
	minVertexCover = graph.minimumVertexCover()
	for side, index in minVertexCover:
		if side == 1:
			common.append(leftEdges[index])
		else:
			common.append(rightEdges[index])
	# sanity check for no repetition in answer
	commonSet = set(common)
	assert len(common) == len(commonSet)
	return common

# import os
# script_dir = os.path.dirname(__file__)
# rel_path = "tests/test2.txt"
# abs_file_path = os.path.join(script_dir, rel_path)

# inputgraph = UncertainGraph()
# inputgraph.buildFromFile(abs_file_path)
# print(inputgraph.edges)
# print(optimalQuerySet(inputgraph))