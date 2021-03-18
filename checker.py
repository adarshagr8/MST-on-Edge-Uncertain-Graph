from graph import *
from copy import deepcopy

# checker for query set
def checkQuerySet(g, querySet):
	# build updated graph by querying edges in the query set
	updatedGraph = deepcopy(g)
	for e in updatedGraph.edges:
		if e in querySet:
			e.query()
	# find lower limit MST in updates graph
	lowerEdges = sorted(list(updatedGraph.edges), key = lambda x: x.lower)
	lowerGraph = Graph(lowerEdges)
	candidateMST = lowerGraph.kruskalMST()
	# check if this lower limit MST stays an MST for all valid realizations
	# But what if lower limit MST isn't unique? Then, all edges not present in all lower limit MSTs must be trivial
	# => All possible MSTs can be converted to one another by swapping trivial edges only
	# => Swapped edges are always maximal and trivial
	# => If a lower limit MST stays an MST for all realizations, all lower limit MSTs stay an MST for all realizations
	# => So checking only one lower limit MST is sufficient
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
	print(querySet)
	print(g)
	print(checkQuerySet(g, querySet))
	return checkQuerySet(g, querySet) and len(querySet) == len(bruteOPT(g))

