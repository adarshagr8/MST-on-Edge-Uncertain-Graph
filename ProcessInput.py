import numpy as np
from numpy import random

d = 0.08
nodes = [10]
edges = []
adjList = {}
f = open("./tests/USARoadDataSet.gr", "r+")
count = 0

for line in f:
    u, v, lo, hi, actual, cost = map(int, line.split())
    if u not in adjList:
        adjList[u] = []
    if v not in adjList:
        adjList[v] = []
    if lo == actual:
        lo = actual - random.randint(1, 3)
        hi = actual + random.randint(1, 3)
    adjList[u].append(v)
    adjList[v].append(u)
    edges.append([u, v, lo, hi, actual, cost])

# def removeMultiEdges():
#     global edges
#     edgeDic = {}
#     for e in edges:
#         edgeDic[(min(e[0], e[1]), max(e[0], e[1]))] = e
#     newEdges = []
#     for e in edgeDic.values():
#         newEdges.append(e)
#     edges = newEdges

# removeMultiEdges()

def generateGraphs():
    global count
    for n in nodes:
        newContent = []
        degree = {}
        values = set()
        g = open("./tests/USA" + str(n) + ".gr", "w+")
        edge = 0
        count = 0
        visited = set()

        def dfs(u):
            global count
            if u in visited:
                return
            if count >= n:
                return
            count += 1
            visited.add(u)
            for v in adjList[u]:
                dfs(v)

        randNode = random.choice(list(adjList.keys()))
        dfs(randNode)

        nodeList = list(visited)
        nodeList.sort()
        nodeId = {}
        edgeSet = set()
        id = 1
        for i in nodeList:
            nodeId[i] = id 
            id += 1

        for line in edges:
            if line[0] not in visited or line[1] not in visited:
                continue
            edge += 1
            degree[line[0]] = degree.get(line[0], 0) + 1
            degree[line[1]] = degree.get(line[1], 0) + 1
            edgeSet.add(line[2])
            edgeSet.add(line[3])
            edgeSet.add(line[4])
            line.pop()
            newContent.append(line)

        g.write(str(count) + " " + str(edge) + "\n")

        edgeList = list(edgeSet)
        edgeList.sort()
        edgeId = {}
        id = 1
        for i in edgeList:
            edgeId[i] = id 
            id += 1
        mxDeg = 0
        for i in range(len(newContent)):
            line = newContent[i]
            deg = (degree[line[0]] + degree[line[1]]) * 0.5
            mxDeg = max(mxDeg, deg)
            newContent[i].append(deg)

        BASE = 100
        e = 0.1

        for i in range(len(newContent)):
            line = newContent[i]
            cost = BASE + (line[5] / mxDeg) * 4 * BASE
            cost = random.randint((1 - e) * cost, (1 + e) * cost)
            newContent[i][5] = cost
            newContent[i][0] = nodeId[newContent[i][0]]
            newContent[i][1] = nodeId[newContent[i][1]]
            newContent[i][2] = edgeId[newContent[i][2]]
            newContent[i][3] = edgeId[newContent[i][3]]
            newContent[i][4] = edgeId[newContent[i][4]]
            newContent[i] = ' '.join(map(str, newContent[i]))

        # print(newContent)
        g.write('\n'.join(newContent))
        g.close()

