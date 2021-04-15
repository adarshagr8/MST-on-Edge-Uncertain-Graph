from graph import *
from copy import deepcopy

eps = 1e-9
# checker for query set
def checkQuerySet(g, querySet):
	# build updated graph by querying edges in the query set
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
	# find a candidate uncertain MST in updated graph
	# we only care about non-trivial edges of uncertain MST as trivial edges can be interchanged
	# for this we need to assign unique weights to all non-trivial edges in a particular realization
	# It is easy to prove that such a realization always exists using the fact that open intervals contain infinite no of points
	# and intersection of two open intervals if it exists is also open.
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
				
	lowerEdges = sorted(list(updatedGraph.edges), key = lambda x: x.actual)
	lowerGraph = Graph(lowerEdges)
	candidateMST = lowerGraph.kruskalMST()
	# check if this candidate MST stays an MST for all valid realizations
	# but what if the answer isn't unique? Then all possible answers will have non-trivial edges in common.
	# => All possible uncertain MSTs can be converted to one another by swapping trivial edges only
	# => So checking only one candidate MST is sufficient
	# To check this, all non-MST edges must be always-maximal but not necessarily in a strict sense (i.e. >= is fine)
	outsideEdges = []
	for e in updatedGraph.edges:
		if e not in candidateMST:
			outsideEdges.append(e)

	lowerTree = DynamicForest(updatedGraph.size)
	for e in candidateMST:
		# sanity check for no cycle in lower MST
		assert not lowerTree.cycleCheck(e)
		lowerTree.addEdge(e)

	for e in outsideEdges:
		cycle = lowerTree.getCycle(e)
		# sanity check for cycle
		assert len(cycle) > 1
		for i in range(1, len(cycle)):
			if cycle[i].upper > cycle[0].lower:
				return False
	return True


def bruteOPT(g):
	nonTrivialEdges = []
	optimalSet = []
	for e in g.edges:
		if not e.trivial:
			optimalSet.append(e)
			nonTrivialEdges.append(e)

	n = len(nonTrivialEdges)
	for mask in range(1 << n):
		querySet = []
		for j in range(n):
			if mask & (1 << j):
				querySet.append(nonTrivialEdges[j])
		if checkQuerySet(g, querySet) and len(querySet) < len(optimalSet):
			optimalSet = querySet
	return optimalSet



def checkOPT(g, querySet):
	# print(bruteOPT(g))
	# assert len(querySet) == len(bruteOPT(g))
	return checkQuerySet(g, querySet) and len(querySet) == len(bruteOPT(g))

