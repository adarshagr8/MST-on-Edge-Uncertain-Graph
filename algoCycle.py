import graph
from preprocessing import Preprocessor
from collections import deque

class CycleModel:
	def __init__(self, g):
		self.G = g
		self.queryCount = 0
		p = Preprocessor(g)
		self.Q = p.query
		self.Tl = p.Tl
		self.Tu = p.Tu
		f = self.G.edges
		for edge in Tl:
			f.remove(edge)

		def dfs(u, par, adj, C):
			for v in adj[u]:
				if v.v != par:
					C.append(v)
					dfs(v.v, u, parents, adj)

		def check(edgeSet):
			if len(edgeSet) <= 1:
				return False
			uppers = []
			for edge in edgeSet:
				uppers.append(edge.upper)
			uppers.sort()
			for edge in edgeSet:
				if edge.upper == uppers[-1] and (edge.trivial or edge.lower >= uppers[-2]):
					return False
			return True

		for edge in f:
			adj = [[] for _ in range(self.G.size + 1)]
			for edge in Tl:
				adj[edge.u].append(edge)
				adj[edge.v].append(edge)
			C = []
			dfs(edge.u, -1, adj, C)
			C.append(edge)
			while check(C):
				uppers = []
				firstUpper = 0
				firstEdge = 0
				for i in range(len(C)):
					if C[i].upper > firstUpper:
						firstUpper = C[i].upper
						firstInd = i
				secondUpper = 0
				secondInd = 0
				firstEdge = C[firstInd]
				for i in range(len(C)):
					if i == firstInd:
						continue
					if C[i].upper > secondUpper:
						secondUpper = C[i].upper
						secondInd = i
				secondEdge = C[secondInd]
				if not firstEdge.trivial:
					self.G.query(firstEdge)
					C.remove(firstEdge)
					firstEdge.lower = firstEdge.actual
					firstEdge.upper = firstEdge.actual
					C.append(firstEdge)
				if not secondEdge.trivial:
					self.G.query(secondEdge)
					C.remove(secondEdge)
					secondEdge.lower = secondEdge.actual
					secondEdge.upper = secondEdge.actual
					C.append(secondEdge)
			if len(C):
				uppers = []
				for edge in edgeSet:
					uppers.append(edge.upper)
				uppers.sort()
				for edge in edgeSet:
					if edge.upper == uppers[-1] and (edge.trivial or edge.lower >= uppers[-2]):
						Tl.erase(edge)
						break
