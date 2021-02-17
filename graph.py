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
            self.addEdge(e.u, e.v)
            
    def addEdge(self, a, b):
        self.adj[a].append(b)
        self.adj[b].append(a)
        self.edges.append((a,b))
    
    def kruskalMST(self):
        comps = UnionFind(self.size + 1)
        mstEdges = []
        for e in self.edges:
            if comps.unite(e[0], e[1]):
                mstEdges.append(e)
        return mstEdges
    
class UncertainEdge:
    def __init__(self, u, v, lower, upper, actual):
        self.u = u
        self.v = v
        self.lower = lower
        self.upper = upper
        self.actual = actual
    
    
    
class UncertainGraph:
    def __init__(self):
        self.edges = []
        
    def buildFromInput(self):
        self.size = int(input("Enter number of nodes: "))
        m = int(input("Enter number of edges: "))
        for i in range(m):
            u, v, lower, upper, actual = list(map(int, input("Enter edge " + str(i + 1) + " : ").split()))
            self.edges.append(UncertainEdge(u, v, lower, upper, actual))

    def output(self):
        print(self.size)
        print(self.edges)
        
    
    
class UncertainMSTSolver(UncertainGraph):
    def __init__(self, g):
        super(UncertainGraph,g)

# g = UncertainGraph()
# g.buildFromInput()
# x = UncertainMSTSolver(g)
# print(x)