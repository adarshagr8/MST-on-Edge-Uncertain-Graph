from collections import deque

class BipartiteGraph:
    def __init__(self, edges):
        n = m = 0
        for e in edges:
            if e[0] > n:
                n = e[0]
            if e[1] > m:
                m = e[1]

        self.leftSize = n + 1
        self.rightSize = m + 1
        self.adj = [[] for i in range(n + 1)]
        self.rightToLeft = [-1 for i in range(m + 1)]
        self.leftToRight = [-1 for i in range(n + 1)]
        self.layerA = [0 for i in range(n + 1)]
        self.layerB = [0 for i in range(m + 1)]
        for e in edges:
            self.addEdge(e[0], e[1])
        # print("n is", n, " and m is", m)
        # print("adj is", self.adj)
        # print("rightToLeft is", self.rightToLeft)

    def addEdge(self, a, b):
        # print("Adding edge from", a, "to", b)
        self.adj[a].append(b)

    def dfs(self, a, L):
        if self.layerA[a] != L:
            return 0
        for b in self.adj[a]:
            if self.layerB[b] == L + 1:
                self.layerB[b] = 0;
                if self.rightToLeft[b] == -1:
                    self.rightToLeft[b] = a
                    return 1
                if self.dfs(self.rightToLeft[b], L + 1) != 0:
                    self.rightToLeft[b] = a
                    return 1
        return 0

    def maximumMatching(self):
        res = 0
        cur = []
        nxt = []
        while True:
            self.layerA = [0 for i in range(self.leftSize)]
            self.layerB = [0 for i in range(self.rightSize)]
            
            # Find the starting nodes for BFS (i.e. layer 0).
            cur.clear()
            for a in self.rightToLeft:
                if a != -1:
                    self.layerA[a] = -1
        
            for a in range(len(self.adj)):
                if self.layerA[a] == 0:
                    cur.append(a)
            
            # print("res is", res)
            # print("cur is", cur)
            # print("nxt is", nxt)
            # print("btoa is", self.rightToLeft)
            # print("layerA is", self.layerA)
            # print("layerB is", self.layerB)
            # Find all layers using BFS
            lay = 1 
            while True:
                isLast = False
                nxt.clear()
                
                for a in cur:
                    for b in self.adj[a]:
                        if self.rightToLeft[b] == -1:
                            isLast = True
                            self.layerB[b] = lay
                        elif self.rightToLeft[b] != a and self.layerB[b] == 0:
                            self.layerB[b] = lay
                            nxt.append(self.rightToLeft[b])
                            
                # print("lay is", lay)
                # print("isLast is", isLast)
                # print("nxt is", nxt)
                if isLast:
                    break
                if len(nxt) == 0:
                    return res

                for a in nxt:
                    self.layerA[a] = lay

                cur, nxt = nxt, cur
                lay += 1

            # Use DFS to scan for augmenting paths
            for a in range(len(self.adj)):
                res += self.dfs(a, 0)

    def minimumVertexCover(self):
        self.maximumMatching()
        left = set()
        right = set()
        leftZ = set()
        rightZ = set()
        unmatchedLeft = set()
        vertexcover = []
        for i in range(self.leftSize):
            left.add(i)
            unmatchedLeft.add(i)
        
        for i in range(self.rightSize):
            right.add(i)
        
        for a in self.rightToLeft:
            if a != -1:                
                unmatchedLeft.remove(a)

        for i in range(len(self.rightToLeft)):
            if self.rightToLeft[i] != -1:
                self.leftToRight[self.rightToLeft[i]] = i
        
        bfs = deque()        
        for u in unmatchedLeft:
            bfs.append((1, u))
            leftZ.add(u)
        
        while len(bfs) > 0:
            side, u = bfs.popleft()
            if side == 1:
                for v in self.adj[u]:
                    if v != self.leftToRight[u]:
                        if v not in rightZ:
                            rightZ.add(v)
                            bfs.append((2, v))
            else:
                v = self.rightToLeft[u]
                assert v != -1
                if v not in leftZ:
                    leftZ.add(v)
                    bfs.append((1, v))
        
        for i in left:
            if i not in leftZ:
                vertexcover.append((1, i))
        
        for i in right:
            if i in rightZ:
                vertexcover.append((2, i))
                
        return vertexcover
                
        


# test for maximum matching 
# n, m, k = list(map(int, input().split()))
# edges = []
# for i in range(k):
#     u, v = list(map(int, input().split()))
#     edges.append((u, v))

# graph = BipartiteGraph(edges)
# matchingSize = graph.maximumMatching()
# print(matchingSize)
# matches = []
# for i in range(len(graph.rightToLeft)):
#     if graph.rightToLeft[i] != -1:
#         matches.append((graph.rightToLeft[i], i))

# for i in matches:
#     print(i[0], " ", i[1])
    
# assert matchingSize == len(matches)


# test for minimum vertex cover
n = int(input())
grid = []
for i in range(n):
    grid.append(input())

edges = []
for i in range(n):
    for j in range(n):
        if grid[i][j] == 'o':
            edges.append((i+1, j+1))

graph = BipartiteGraph(edges)
ans = graph.minimumVertexCover()
print(len(ans))
for i in ans:
    print(i[0], " ", i[1])
