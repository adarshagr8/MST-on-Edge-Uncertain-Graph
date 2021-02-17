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
        self.parent[v] = self.findSet(parent[v])
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
        self.size = len(edgeList)
        self.adj = [[] for i in range(n)]
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
    
    
class UncertainGraph:
    def __init__(self):
        self.edges = set()
        
    def buildFromInput(self):
        self.size = int(input("Enter number of nodes: "))
        m = int(input("Enter number of edges: "))
        for i in range(m):
            u, v, lower, upper, actual = list(map(int, input("Enter edge " + str(i + 1) + " : ").split()))
            self.edges.add(UncertainEdge(u, v, lower, upper, actual, i))

    def buildFromFile(self, s):
        f = open(s, "r")
        self.size = int(f.readline())
        m = int(f.readline())
        for i in range(m):
            u, v, lower, upper, actual = map(int, f.readline().split())
            self.edges.add(UncertainEdge(u, v, lower, upper, actual, i))

    def query(self, edge):
        self.edges.erase(edge)
        edge.lower = edge.actual
        edge.upper = edge.actual
        self.edge.add(edge)
        
    def output(self):
        print(self.size)
        print(self.edges)
