import graph

class Preprocessor:
	def __init__(self, g):
		self.query = set()
		self.G = g
		edgeSet = self.G.edges
		Tl = lowerLimitTree(edgeSet)
		Tu = upperLimitTree(edgeSet)
		newEdge = findIntersection(Tl, Tu)
		while len(newEdge):
			for edge in newEdge:
				query.add(edge)
				edgeSet.erase(edge)
			Tl = lowerLimitTree(edgeSet)
			Tu = upperLimitTree(edgeSet)
			newEdge = findIntersection(Tl, Tu)

	def lowerOrderingComparator(e1, e2):
		if e1.lower != e2.lower:
			return e1.lower - e2.lower
		else:
			if e1.trivial and not e2.trivial:
				return -1
			if not e1.trivial and e2.trivial:
				return 1
			if e1.trivial and e2.trivial:
				return e1.index - e2.index
			if e1.upper != e2.upper:
				return e2.upper - e1.upper
		return e1.index - e2.index

	def upperOrderingComparator(e1, e2):
		if e1.upper != e2.upper:
			return e1.upper - e2.upper
		else:
			if e1.trivial and not e2.trivial:
				return -1
			if not e1.trivial and e2.trivial:
				return 1
			if e1.trivial and e2.trivial:
				return e1.index - e2.index
			if e1.lower != e2.lower:
				return e2.lower - e1.lower
		return e1.index - e2.index

	def lowerLimitTree(edges):
		lowerEdgeOrdering = sorted(edges, key = cmp_to_key(lowerOrderingComparator))
		g = Graph(lowerEdgeOrdering)
		return g.kruskalMST()

	def upperLimitTree(edges):
		upperEdgeOrdering = sorted(edges, key = cmp_to_key(upperOrderingComparator))
		g = Graph(upperEdgeOrdering)
		return g.kruskalMST()

	def findIntersection(tl, tu):
		ans = set()
		for edge in tl:
			if edge not in tu and not edge.trivial:
				ans.add(edge)
		return ans
