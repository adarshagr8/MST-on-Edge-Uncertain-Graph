# MST-on-Edge-Uncertain-Graph

### Introduction
The project was aimed towards fulfillment of B.Tech Project Requirements Third Year B.Tech. We consider the problem of finding a minimum spanning tree of a graph where some of the edge weights are unknown and only their upper and lower bounds are available, but these edges can be explored to reveal their actual weight at an extra cost. The goal here is to find the Minimum Spanning Tree (MST) of an edge-uncertain graph by exploring the minimum number of edges. We compare the performances of two online greedy algorithms with that of an optimal algorithm, which utilizes the information about actual weights of the uncertain edges to find the minimum number of queries needed to narrow down the MST. 

## How to run?

Run the python file "main.py" in order to run the code first against manual test cases. The program will prompt for the number of random test cases to be generated next and would execute against randomly generated testcases with _|V|_ = 100 and _|E| ∈ [100, 200]_ .

## File Description
Here we will describe the function of each file:
| File Name      | Function |
| ----------- | ----------- |
| main.py      | Main File of the program which uses other file to generate output       |
| graph.py   | Base definition of underlying data structures: Graph, UncertainGraph, UncertainEdge, UnionFind, DynamicForest        |
| checker.py | Validation code to check whether the query set in output is feasible or not |
| generator.py | Generating all sorts of different graphs to check confirm the correctness of the algorithm |
| preprocessing.py | Preprocessing code that generates a query set that must be queried for any algorithm to be used next |
| optimal.py | Optimal Algorithm which generates the minimum possible query set for the given uncertain graph |
| algoCycle.py | The first greedy algorithm to be tested |
| algoCut.py | The second greedy algorithm to be tested |
| bipartite.py | |
