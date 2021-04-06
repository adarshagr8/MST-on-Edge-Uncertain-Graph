from graph import *
from functools import cmp_to_key
from copy import deepcopy

class Preprocessor:
	def __init__(self, g):
		self.query = set()
		self.G = deepcopy(g)
		self.Tl = self.lowerLimitTree()
		self.Tu = self.upperLimitTree()
		newEdge = self.findIntersection(self.Tl, self.Tu)
		while len(newEdge):
			for edge in newEdge:
				self.G.query(edge)
			self.Tl = self.lowerLimitTree()
			self.Tu = self.upperLimitTree()
			newEdge = self.findIntersection(self.Tl, self.Tu)

	def lowerOrderingComparator(self, e1, e2):
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

	def upperOrderingComparator(self, e1, e2):
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

	def lowerLimitTree(self):
		lowerEdgeOrdering = sorted(self.G.edges, key = cmp_to_key(self.lowerOrderingComparator))
		g = Graph(lowerEdgeOrdering)
		return g.kruskalMST()

	def upperLimitTree(self):
		upperEdgeOrdering = sorted(self.G.edges, key = cmp_to_key(self.upperOrderingComparator))
		g = Graph(upperEdgeOrdering)
		return g.kruskalMST()

	def findIntersection(self, tl, tu):
		ans = set()
		for edge in tl:
			if edge not in tu and not edge.trivial:
				ans.add(edge)
		return ans
