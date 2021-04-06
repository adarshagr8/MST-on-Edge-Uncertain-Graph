class UnionFind:
    def __init__(self, n):
        self.parent = [0]*n
        self.size = [0]*n
        for i in range(n):
            self.makeSet(i)

    def makeSet(self, v):
        self.parent[v] = v
        self.size[v] = 1

    def findSet(self, v):
        if self.parent[v] == v:
            return v
        self.parent[v] = self.findSet(self.parent[v])
        return self.parent[v]

    def unite(self, a, b):
        a = self.findSet(a)
        b = self.findSet(b)
        if a == b:
            return False
        if self.size[a] < self.size[b]:
            tmp = a
            a = b
            b = tmp
        self.parent[b] = a
        self.size[a] += self.size[b]
        return True


class Graph:
    def __init__(self, edgeList):
        self.size = 0
        self.edges = []
        for e in edgeList:
            self.size = max(self.size, e.u)
            self.size = max(self.size, e.v)
        self.adj = [[] for i in range(self.size + 1)]
        for e in edgeList:
            self.addEdge(e)

    def addEdge(self, edge):
        self.adj[edge.u].append(edge.v)
        self.adj[edge.v].append(edge.u)
        self.edges.append(edge)

    def kruskalMST(self):
        comps = UnionFind(self.size + 1)
        mstEdges = set()
        for e in self.edges:
            if comps.unite(e.u, e.v):
                # print(e)
                mstEdges.add(e)
        return mstEdges


class UncertainEdge:
    def __init__(self, u, v, lower, upper, actual, index):
        self.u = u
        self.v = v
        self.lower = lower
        self.upper = upper
        self.actual = actual
        self.index = index
        self.trivial = (lower == upper)

    def query(self):
        self.lower = self.upper = self.actual
        self.trivial = True
        return self.actual

    def __str__(self):
        return str(self.u) + ' ' + str(self.v) + ' ' + str(self.lower) + ' ' + str(self.upper) + ' ' + str(self.actual)

    __repr__ = __str__

    def __eq__(self, other):
        return (self.u, self.v, self.lower, self.upper, self.actual, self.index) == (other.u, other.v, other.lower, other.upper, other.actual, other.index)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.u, self.v, self.lower, self.upper, self.actual, self.index))


class UncertainGraph:
    def __init__(self):
        self.edges = set()

    def buildFromParameters(self, n, edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual):
        self.size = n
        m = len(edgeFrom)
        assert len(edgeTo) == m and len(edgeLo) == m and len(
            edgeHi) == m and len(edgeActual) == m
        for i in range(m):
            self.edges.add(UncertainEdge(
                edgeFrom[i], edgeTo[i], edgeLo[i], edgeHi[i], edgeActual[i], i))

    def buildFromInput(self):
        self.size = int(input("Enter number of nodes: "))
        m = int(input("Enter number of edges: "))
        for i in range(m):
            u, v, lower, upper, actual = list(
                map(int, input("Enter edge " + str(i + 1) + " : ").split()))
            self.edges.add(UncertainEdge(u, v, lower, upper, actual, i))

    def buildFromFile(self, s):
        f = open(s, "r")
        self.size, m = map(int, f.readline().split())

        for i in range(m):
            u, v, lower, upper, actual = map(int, f.readline().split())
            self.edges.add(UncertainEdge(u, v, lower, upper, actual, i))

    def query(self, edge):
        # self.edges.remove(edge)
        edge.query()
        # self.edges.add(edge)

    def output(self):
        print(self.size)
        print(self.edges)

    def __str__(self):
        return str(self.edges)

    __repr__ = __str__


class DynamicForest:
    def __init__(self, n):
        self.size = n
        self.edges = set()
        self.adj = [set() for i in range(n + 1)]
        self.comps = UnionFind(n + 1)

    def addEdge(self, edge):
        self.adj[edge.u].add(edge)
        self.adj[edge.v].add(edge)
        self.edges.add(edge)
        self.comps.unite(edge.u, edge.v)

    def removeEdge(self, edge):
        self.adj[edge.u].discard(edge)
        self.adj[edge.v].discard(edge)
        self.edges.discard(edge)
        self.comps = UnionFind(self.size + 1)
        for e in self.edges:
            self.comps.unite(e.u, e.v)

    def cycleCheck(self, edge):
        return self.comps.findSet(edge.u) == self.comps.findSet(edge.v)

    def dfs(self, node, target, cycleEdges, par):
        if node == target:
            return 1
        for e in self.adj[node]:
            other = e.v
            if other == node:
                other = e.u
            if other == par:
                continue
            if self.dfs(other, target, cycleEdges, node):
                cycleEdges.append(e)
                return 1
        return 0

    def getCycle(self, edge):
        cycleEdges = [edge]
        self.dfs(edge.u, edge.v, cycleEdges, -1)
        return cycleEdges
