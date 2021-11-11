from collections import deque

class FlowEdge:
    """Stores edge info for flow graph"""
    def __init__(self, to, rev, cap, flow):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.flow = flow
        
class ScaledDinic:
    """Finds max flow in a given graph in V * E * log(Flow) time."""
    def __init__(self, edges, source, sink):
        """Takes a collection of edges (described by 3-tuples)"""
        self.source = source
        self.sink = sink
        self.inf = 1
        for e in edges:
            self.inf += e[2]
        self.inf *= 1024
        self.lim = 1
        self.size = sink + 1
        self.level = [0 for i in range(self.size)]
        self.ptr = [0 for i in range(self.size)]
        self.adj = [[] for i in range(self.size)]
        for e in edges:
            self.addEdge(e[0], e[1], e[2])
        # print("Initialization done!")


    def addEdge(self, a, b, cap):
        self.adj[a].append(FlowEdge(b, len(self.adj[b]), cap, 0))
        self.adj[b].append(FlowEdge(a, len(self.adj[a]) - 1, 0, 0))

    def dfs(self, v, flow):
        if v == self.sink or flow == 0:
            return flow
        while self.ptr[v] < len(self.adj[v]):
            e = self.adj[v][self.ptr[v]]
            if self.level[e.to] != self.level[v] + 1:
                self.ptr[v] += 1
                continue
            pushed = self.dfs(e.to, min(flow, e.cap - e.flow))
            if pushed > 0:
                e.flow += pushed
                self.adj[e.to][e.rev].flow -= pushed
                return pushed
            self.ptr[v] += 1
        return 0


    def bfs(self):
        q = deque()
        q.append(self.source)
        self.level = [-1 for i in range(self.size)]
        self.level[self.source] = 0
        while len(q) > 0 and self.level[self.sink] == -1:
            v = q.popleft()
            for e in self.adj[v]:
                if self.level[e.to] == -1 and e.flow < e.cap and e.cap - e.flow >= self.lim:
                    q.append(e.to);
                    self.level[e.to] = self.level[v] + 1;

        return self.level[self.sink] != -1

    def calcMaxFlow(self):
        flow = 0
        while self.lim <= self.inf:
            self.lim *= 2

        # print(self.lim)
        while self.lim > 0:
            while self.bfs():
                self.ptr = [0 for i in range(self.size)]
                while True:
                    pushed = self.dfs(self.source, self.inf)
                    # print("pushed", pushed)
                    flow += pushed
                    if pushed == 0:
                        break
            self.lim = self.lim // 2
        return flow




class WeightedBipartiteGraph:
    """Supports finding minimum weight vertex cover in vertex weighted bipartite graphs"""
    def __init__(self, edges, weightsA, weightsB):
        """Takes in a collection of edges (described by 2-tuples) and vertex weights to build the bipartite graph."""
        n = len(weightsA)
        m = len(weightsB)

        self.leftSize = n
        self.rightSize = m
        self.size = n + m + 3
        self.source = n + m + 1
        self.sink = n + m + 2
        flowGraphEdges = []
        # build flow graph
        inf = 1
        cur = 1
        for a in weightsA:
            inf += a
            flowGraphEdges.append((self.source, cur, a))
            cur += 1

        cur = 1
        for b in weightsB:
            flowGraphEdges.append((n + cur, self.sink, b))
            cur += 1
        
        for e in edges:
            flowGraphEdges.append((e[0], n + e[1], inf))
        
        self.flowGraph = ScaledDinic(flowGraphEdges, self.source, self.sink)
        # print("n is", n, " and m is", m)
        # print("adj is", self.adj)
        # print("rightToLeft is", self.rightToLeft)

    def addEdge(self, a, b, c):
        # print("Adding edge from", a, "to", b, "with capacity", c)
        self.adj[a].append((b, c))

    def maxFlow(self):
        self.flowGraph.calcMaxFlow()


    def markVis(self, v):
        if self.visited[v] == 1:
            return
        self.visited[v] = 1
        for e in self.flowGraph.adj[v]:
            if e.cap - e.flow > 0:
                self.markVis(e.to)



    def minCut(self):
        self.maxFlow()
        # mark visited
        self.visited = [0 for i in range(self.size)]
        self.markVis(self.source)
        assert self.visited[self.sink] == 0
        # build CS and CT sets
        CS = []
        CT = []
        for e in self.flowGraph.adj[self.source]:
            if self.visited[e.to] == 0 and e.cap > 0:
                CS.append(e.to)

        for i in range(self.size):
            if self.visited[i] == 0:
                continue
            for e in self.flowGraph.adj[i]:
                if e.cap == 0:
                    continue
                if e.to == self.sink:
                    CT.append(i)

        return CS, CT

    def minimumVertexCover(self):
        CS, CT = self.minCut()
        vertexCover = []
        for i in CS:
            vertexCover.append((1, i))

        for i in CT:
            vertexCover.append((2, i - self.leftSize))
        return vertexCover



# test for minimum vertex cover
# n = int(input())
# grid = []
# for i in range(n):
#     grid.append(input())

# edges = []
# for i in range(n):
#     for j in range(n):
#         if grid[i][j] == 'o':
#             edges.append((i+1, j+1))

# nweight = [1 for i in range(n)]
# mweight = [1 for i in range(n)]
# graph = WeightedBipartiteGraph(edges, nweight, mweight)
# ans = graph.minimumVertexCover()
# print(len(ans))
# for i in ans:
#     print(i[0], " ", i[1])


# test for maximum flow
# n, m = list(map(int, input().split()))
# edges = []
# for i in range(m):
#     a, b, c = list(map(int, input().split()))
#     edges.append((a, b, c))

# Dinic = ScaledDinic(edges, 1, n)
# print(Dinic.calcMaxFlow())


