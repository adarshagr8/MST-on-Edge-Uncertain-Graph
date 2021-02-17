import graph
import bipartite

def compareEdges(e, f):
	if e.lower != f.lower:
		return e.lower - f.lower
	elif e.upper != f.lower:
		return e.upper - f.upper
	else:
		return 0


def optimalQuerySet(g):

	# PHASE 1
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
		if not curgraph.cycleCheck(e):
			curgraph.addEdge(e)
			continue
		cycle = curgraph.getCycle(e)
		curgraph.addEdge(e)
		# check case (a)
		bool hasMaximal = True
		candidate = cycle[0]
		for e in cycle:
			if e.upper > candidate.upper:
				candidate = e

		for e in cycle:
			if e.upper > candidate.lower:
				hasMaximal = False

		if hasMaximal:
			curgraph.removeEdge(candidate)
			continue

		# check case (b)
		bool flag = False
		for e in cycle:
			if e.actual > candidate.actual:
				flag = True
				break

		if not flag:
			for e in cycle:
				if e.upper > candidate.actual and e != candidate:
					flag = True
					candidate = e
					break

		if not flag:
			for e in cycle:
				if e.actual > candidate.lower and e != candidate:
					flag = True
					break

		if flag:
			# update candidate, remove from curgraph and add to common and back to sortedEdges
			curgraph.removeEdge(candidate)
			common.append(curgraph)
			candidate.query()
			sortedEdges.append(candidate)
			sortedEdges = sorted(sortedEdges, key = cmp_to_key(compareEdges))
			continue
		# check case (c)
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
	# build bipartite graph
	leftEdgeToIndex = {}
	leftEdges = []
	for d, B in choices:
		leftEdgeToIndex[d] = len(leftEdges)
		leftEdges.append(d)

	choiceUnion = set()
	for d, B in choices:
		for e in B:
			choiceUnion.add(e)

	rightEdges = list(choiceUnion)
	rightEdgeToIndex = {}
	for e in rightEdges:
		rightEdgeToIndex[e] = len(rightEdgeToIndex)

	edgesInGprime = []
	for d, B in choices:
		for e in B:
			edgesInGprime.append((leftEdgeToIndex[d], rightEdgeToIndex[e]))

	graph = BipartiteGraph(edgesInGprime)
	# find minimum vertex cover and recover solution from it and return
	minVertexCover = graph.minimumVertexCover()
	for side, index in minVertexCover:
		if side == 1:
			common.append(leftEdges[index])
		else:
			common.append(rightEdges[index])
	return common