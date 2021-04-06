import graph
from preprocessing import Preprocessor
from collections import deque
from copy import deepcopy


class CycleModel:
    def __init__(self, g):
        self.G = deepcopy(g)
        self.queryCount = 0
        p = Preprocessor(g)
        # print("Preprocessing:", p.query)
        self.Q = deepcopy(p.query)
        self.Tl = deepcopy(p.Tl)
        self.Tu = deepcopy(p.Tu)
        f = self.G.edges
        removed = set()
        for edge in self.Tl:
            removed.add((edge.u, edge.v))
        erased = set()
        for edge in f:
            if (edge.u, edge.v) in removed or (edge.v, edge.u) in removed:
                erased.add(edge)
        for edge in erased:
            f.remove(edge)
        # print("f: ", f)
        C = []

        def dfs(u, par, adj, last, edges):
            if u == last:
                C[:] = edges
            for v in adj[u]:
                if v.u + v.v - u != par:
                    edges.append(v)
                    dfs(v.u + v.v - u, u, adj, last, edges)
                    edges.remove(v)

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
            # print("Tl:", self.Tl)
            # print("Added Edge:", edge)
            adj = [[] for _ in range(self.G.size + 1)]
            for edge2 in self.Tl:
                adj[edge2.u].append(edge2)
                adj[edge2.v].append(edge2)
            C[:] = []
            # print(edge.u, adj)
            dfs(edge.u, -1, adj, edge.v, [])
            C.append(edge)
            # print("Cycle: ", C)
            self.Tl.add(edge)
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
                # print("First: ", firstEdge, "Second: ", secondEdge)
                if not firstEdge.trivial:
                    self.Q.add(deepcopy(firstEdge))
                    self.Tl.remove(firstEdge)
                    self.G.query(firstEdge)
                    C.remove(firstEdge)
                    firstEdge.lower = firstEdge.actual
                    firstEdge.upper = firstEdge.actual
                    firstEdge.trivial = True
                    self.Tl.add(firstEdge)
                    C.append(firstEdge)
                if not secondEdge.trivial:
                    self.Q.add(deepcopy(secondEdge))
                    self.Tl.remove(secondEdge)
                    self.G.query(secondEdge)
                    C.remove(secondEdge)
                    secondEdge.lower = secondEdge.actual
                    secondEdge.upper = secondEdge.actual
                    secondEdge.trivial = True
                    self.Tl.add(secondEdge)
                    C.append(secondEdge)
                # print(C)

            if len(C):
                uppers = []
                for edge in C:
                    uppers.append(edge.upper)
                uppers.sort()
                uCon, vCon = None, None
                for edge in C:
                    if edge.upper == uppers[-1] and (edge.trivial or edge.lower >= uppers[-2]):
                        self.Tl.remove(edge)
                        # print("Removed Edge:", edge)
                        break
