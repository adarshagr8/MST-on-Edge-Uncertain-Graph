import graph
from preprocessing import Preprocessor
from collections import deque
from copy import deepcopy


class CutModel:
    def __init__(self, g):
        self.G = deepcopy(g)
        self.queryCount = 0
        p = Preprocessor(self.G)
        # print("Preprocessing:", p.query)
        self.Q = deepcopy(p.query)
        self.Tl = deepcopy(p.Tl)
        self.Tu = deepcopy(p.Tu)
        g = list(deepcopy(self.Tu))
        g.sort(key=lambda x: -x.upper)
        # print("g: ", g)
        component = {}

        def dfs(u, par, adj, c):
            component[u] = c
            for v in adj[u]:
                if v.u + v.v - u != par:
                    dfs(v.u + v.v - u, u, adj, c)

        def check(edgeSet):
            if len(edgeSet) <= 1:
                return False
            lowers = []
            for edge in edgeSet:
                lowers.append(edge.lower)
            lowers.sort()
            for edge in edgeSet:
                if edge.lower == lowers[0] and (edge.trivial or edge.upper <= lowers[1]):
                    return False
            return True

        for edge in g:
            # print("Tu:", self.Tu)
            # print("Removed Edge:", edge)
            adj = [[] for _ in range(self.G.size + 1)]
            erased = None
            for edge2 in self.Tu:
                if {edge2.u, edge2.v} == {edge.u, edge.v}:
                    erased = edge2
            self.Tu.remove(erased)
            for edge2 in self.Tu:
                adj[edge2.u].append(edge2)
                adj[edge2.v].append(edge2)
            # print("f:", f)
            # print(edge.u, adj)
            component.clear()
            dfs(edge.u, -1, adj, 0)
            dfs(edge.v, -1, adj, 1)
            # print(component)
            C = []
            for edge2 in self.G.edges:
                # print(edge, component[edge.u], component[edge.v])
                if component[edge2.u] != component[edge2.v]:
                    C.append(edge2)
            # print("C: ", C)
            while check(C):
                # print("C:", C)
                firstLower = 1e9
                firstInd = 0
                for i in range(len(C)):
                    if C[i].lower < firstLower:
                        firstLower = C[i].lower
                        firstInd = i
                secondLower = 1e9
                secondInd = 0
                firstEdge = C[firstInd]
                for i in range(len(C)):
                    if i == firstInd:
                        continue
                    if C[i].lower < secondLower:
                        secondLower = C[i].lower
                        secondInd = i
                secondEdge = C[secondInd]
                assert secondEdge.lower <= firstEdge.upper
                # print("First: ", firstEdge, "Second: ", secondEdge)
                if not firstEdge.trivial:
                    self.Q.add(deepcopy(firstEdge))
                    self.G.query(firstEdge)
                    C.remove(firstEdge)
                    firstEdge.lower = firstEdge.actual
                    firstEdge.upper = firstEdge.actual
                    firstEdge.trivial = True
                    C.append(firstEdge)
                if not secondEdge.trivial:
                    self.Q.add(deepcopy(secondEdge))
                    self.G.query(secondEdge)
                    C.remove(secondEdge)
                    secondEdge.lower = secondEdge.actual
                    secondEdge.upper = secondEdge.actual
                    secondEdge.trivial = True
                    C.append(secondEdge)

            if len(C):
                if len(C) == 1:
                    self.Tu.add(C[0])
                else:
                    lowers = []
                    for edge in C:
                        lowers.append(edge.lower)
                    lowers.sort()
                    for edge in C:
                        if edge.lower == lowers[0] and (edge.trivial or edge.upper <= lowers[1]):
                            self.Tu.add(edge)
                            # print("Added Edge:", edge)
                            break
