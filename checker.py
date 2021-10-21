from graph import *
from copy import deepcopy

eps = 1e-12
# checker for query set
def checkQuerySet(g, querySet):
	"""Checks the validity of the query set with respect to the given uncertain graph."""
	# Build updated graph by querying edges in the query set first
	updatedGraph = deepcopy(g)
	newQuerySet = set()
	for e in querySet:
		newQuerySet.add(e)

	# print("Query Set: ", querySet, newQuerySet)
	for e in updatedGraph.edges:
		# print(e, e in querySet)
		if e in newQuerySet:
			# print("Found ", e)
			e.query()
	# print("Updated Graph:")
	# print(updatedGraph)

	# Find a candidate uncertain MST in the updated graph
	# For this we need to assign unique weights to all non-trivial edges in a particular realization.
	usedWeights = set()
	for e in updatedGraph.edges:
		if e.trivial:
			usedWeights.add(e.actual)
	for e in updatedGraph.edges:
		if not e.trivial:
			cur = e.lower + eps
			while cur in usedWeights:
				cur += eps
			assert cur < e.upper
			usedWeights.add(cur)
			e.actual = cur
	
	# Sort all edges according to the previously generated realization and find an MST			
	lowerEdges = sorted(list(updatedGraph.edges), key = lambda x: x.actual)
	lowerGraph = Graph(lowerEdges)
	candidateMST = lowerGraph.kruskalMST()
	# Check if this candidate MST stays an MST for all valid realizations
	outsideEdges = []
	for e in updatedGraph.edges:
		if e not in candidateMST:
			outsideEdges.append(e)

	# For this to be true, all outside edges must be maximal (but not necessarily in a strict sense).
	lowerTree = DynamicForest(updatedGraph.size)
	for e in candidateMST:
		# sanity check for no cycle in lower MST
		assert not lowerTree.cycleCheck(e)
		lowerTree.addEdge(e)

	for e in outsideEdges:
		cycle = lowerTree.getCycle(e)
		# sanity check for cycle length
		assert len(cycle) > 1
		# check if the added outside edge is maximal or not
		for i in range(1, len(cycle)):
			if cycle[i].upper > cycle[0].lower:
				return False
	return True


def bruteOPT(g):
	"""Brute force for finding optimal query set for a given uncertain graph."""
	nonTrivialEdges = []
	optimalSet = []
	for e in g.edges:
		if not e.trivial:
			optimalSet.append(e)
			nonTrivialEdges.append(e)

	n = len(nonTrivialEdges)
	# Iterate over all subsets of non-trivial edges and check if it forms a valid query set and update the answer if it does.
	for mask in range(1 << n):
		querySet = []
		for j in range(n):
			if mask & (1 << j):
				querySet.append(nonTrivialEdges[j])
		if checkQuerySet(g, querySet) and getTotalQueryCost(querySet) < getTotalQueryCost(optimalSet):
			optimalSet = querySet
	return optimalSet



def checkOPT(g, querySet):
	"""Checks if the query set is optimal or not with respect to the given uncertain graph."""
	# print(bruteOPT(g))
	# assert len(querySet) == len(bruteOPT(g))
	return checkQuerySet(g, querySet) and getTotalQueryCost(querySet) == getTotalQueryCost(bruteOPT(g))

