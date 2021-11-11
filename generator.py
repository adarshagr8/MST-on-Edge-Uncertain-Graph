from graph import *
from numpy import random
import numpy as np
import random

EPS = 1e-9


class GraphGenerator:
    def __init__(self, debug):
        self.debug = debug

    def getEdgeWeightA(self, lo, hi, centre, deviation, trivialProbability):
        probability = random.uniform(0, 1)
        if probability <= trivialProbability:
            weight = random.uniform(lo, hi)
            return (weight, weight, weight)
        left, right = centre, centre
        length = (hi - lo) * deviation
        left = max(lo, left - length)
        right = min(hi, left + length)
        weight = random.uniform(left, right)
        return (lo, hi, weight)

    def getEdgeWeightB(self, lo, hi, trivialProbability):
        probability = random.uniform(0, 1)
        if probability <= trivialProbability:
            weight = random.uniform(lo, hi)
            return (weight, weight, weight)
        left, right = random.uniform(lo, hi), random.uniform(lo, hi)
        if left > right:
            left, right = right, left
        weight = random.uniform(left, right)
        return (left, right, weight)

    def constructGraphA(self, n, m, lo, hi, centre=None, deviation=0.5, trivialProbability=0.5):
        if lo > hi:
            lo, hi = hi, lo
        if centre == None:
            centre = (lo + hi) / 2
        if n > 1000 or m < n-1 or m > n*(n - 1)//2:
            assert False
        if lo < 0 or hi < lo:
            assert False
        if centre < lo or centre > hi:
            assert False
        if deviation < 0 or deviation > 1:
            assert False
        if trivialProbability < 0 or trivialProbability > 1:
            assert False
        if self.debug:
            print(
                f"Constructing graph with n = {n}, m = {m}, lo = {lo}, hi = {hi}, centre = {centre}, deviation = {deviation} and trivialProbability = {trivialProbability}.")
        if lo != hi:
            lo += EPS
            hi -= EPS
        order = [i for i in range(1, n + 1)]
        order = np.array(order)
        random.shuffle(order)
        order = order.tolist()
        parent = [-1 for i in range(n + 1)]
        edgeSet = set()
        for i in range(1, n):
            parent[order[i]] = order[random.randint(0, i-1)]
        edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual = [], [], [], [], []
        for i in range(1, n):
            edgeFrom.append(order[i])
            edgeTo.append(parent[order[i]])
            edgeSet.add((order[i], parent[order[i]]))
            edgeSet.add((parent[order[i]], order[i]))
            weights = self.getEdgeWeightA(
                lo, hi, centre, deviation, trivialProbability)
            edgeLo.append(weights[0])
            edgeHi.append(weights[1])
            edgeActual.append(weights[2])
        # print(edgeSet)
        m -= (n - 1)
        for i in range(m):
            u, v = random.randint(1, n), random.randint(1, n)
            while u == v or (u, v) in edgeSet:
                u, v = random.randint(1, n), random.randint(1, n)
            edgeFrom.append(u)
            edgeTo.append(v)
            edgeSet.add((u, v))
            edgeSet.add((v, u))
            weights = self.getEdgeWeightA(
                lo, hi, centre, deviation, trivialProbability)
            edgeLo.append(weights[0])
            edgeHi.append(weights[1])
            edgeActual.append(weights[2])
        graph = UncertainGraph()
        graph.buildFromParameters(
            n, edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual)
        return graph

    def constructGraphB(self, n, m, lo, hi, trivialProbability=0.5):
        if lo > hi:
            lo, hi = hi, lo
        if n > 1000 or m < n-1 or m > n*(n - 1)//2:
            assert False
        if lo < 0 or hi < lo:
            assert False
        if trivialProbability < 0 or trivialProbability > 1:
            assert False
        if self.debug:
            print(
                f"Constructing graph with n = {n}, m = {m}, lo = {lo}, hi = {hi}, centre = {centre}, deviation = {deviation} and trivialProbability = {trivialProbability}.")
        if lo != hi:
            lo += EPS
            hi -= EPS
        order = [i for i in range(1, n + 1)]
        order = np.array(order)
        random.shuffle(order)
        order = order.tolist()
        parent = [-1 for i in range(n + 1)]
        edgeSet = set()
        for i in range(1, n):
            parent[order[i]] = order[random.randint(0, i-1)]
        edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual = [], [], [], [], []
        for i in range(1, n):
            edgeFrom.append(order[i])
            edgeTo.append(parent[order[i]])
            edgeSet.add((order[i], parent[order[i]]))
            edgeSet.add((parent[order[i]], order[i]))
            weights = self.getEdgeWeightB(
                lo, hi, trivialProbability)
            edgeLo.append(weights[0])
            edgeHi.append(weights[1])
            edgeActual.append(weights[2])
        # print(edgeSet)
        m -= (n - 1)
        for i in range(m):
            u, v = random.randint(1, n), random.randint(1, n)
            while u == v or (u, v) in edgeSet:
                u, v = random.randint(1, n), random.randint(1, n)
            edgeFrom.append(u)
            edgeTo.append(v)
            edgeSet.add((u, v))
            edgeSet.add((v, u))
            weights = self.getEdgeWeightB(
                lo, hi, trivialProbability)
            edgeLo.append(weights[0])
            edgeHi.append(weights[1])
            edgeActual.append(weights[2])
        graph = UncertainGraph()
        graph.buildFromParameters(
            n, edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual)
        return graph

    def constructGraph2A(self, n, m, lo, hi, centre=None, deviation=0.5, trivialProbability=0.5):
        if lo > hi:
            lo, hi = hi, lo
        if centre == None:
            centre = (lo + hi) / 2
        if n > 1000 or m < n-1 or m > n*(n - 1)//2:
            assert False
        if lo < 0 or hi < lo:
            assert False
        if centre < lo or centre > hi:
            assert False
        if deviation < 0 or deviation > 1:
            assert False
        if trivialProbability < 0 or trivialProbability > 1:
            assert False
        if self.debug:
            print(
                f"Constructing graph with n = {n}, m = {m}, lo = {lo}, hi = {hi}, centre = {centre}, deviation = {deviation} and trivialProbability = {trivialProbability}.")
        if lo != hi:
            lo += EPS
            hi -= EPS
        order = [i for i in range(1, n + 1)]
        order = np.array(order)
        random.shuffle(order)
        order = order.tolist()
        parent = [-1 for i in range(n + 1)]
        edgeSet = set()
        for i in range(1, n):
            parent[order[i]] = order[random.randint(0, i-1)]
        edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual, costs = [], [], [], [], [], []
        for i in range(1, n):
            edgeFrom.append(order[i])
            edgeTo.append(parent[order[i]])
            edgeSet.add((order[i], parent[order[i]]))
            edgeSet.add((parent[order[i]], order[i]))
            weights = self.getEdgeWeightA(
                lo, hi, centre, deviation, trivialProbability)
            edgeLo.append(weights[0])
            edgeHi.append(weights[1])
            edgeActual.append(weights[2])
            costs.append(random.randint(1, n))
        m -= (n - 1)
        for i in range(m):
            u, v = random.randint(1, n), random.randint(1, n)
            while u == v or (u, v) in edgeSet:
                u, v = random.randint(1, n), random.randint(1, n)
            edgeFrom.append(u)
            edgeTo.append(v)
            edgeSet.add((u, v))
            edgeSet.add((v, u))
            weights = self.getEdgeWeightA(
                lo, hi, centre, deviation, trivialProbability)
            edgeLo.append(weights[0])
            edgeHi.append(weights[1])
            edgeActual.append(weights[2])
            costs.append(random.randint(1, n))
        graph = UncertainGraph()
        graph.buildFromParameters(
            n, edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual, costs)
        return graph

    def constructGraph2B(self, n, m, lo, hi, trivialProbability=0.5):
        if lo > hi:
            lo, hi = hi, lo
        if n > 1000 or m < n-1 or m > n*(n - 1)//2:
            assert False
        if lo < 0 or hi < lo:
            assert False
        if trivialProbability < 0 or trivialProbability > 1:
            assert False
        if self.debug:
            print(
                f"Constructing graph with n = {n}, m = {m}, lo = {lo}, hi = {hi} and trivialProbability = {trivialProbability}.")
        if lo != hi:
            lo += EPS
            hi -= EPS
        order = [i for i in range(1, n + 1)]
        order = np.array(order)
        random.shuffle(order)
        order = order.tolist()
        parent = [-1 for i in range(n + 1)]
        edgeSet = set()
        for i in range(1, n):
            parent[order[i]] = order[random.randint(0, i-1)]
        edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual, costs = [], [], [], [], [], []
        for i in range(1, n):
            edgeFrom.append(order[i])
            edgeTo.append(parent[order[i]])
            edgeSet.add((order[i], parent[order[i]]))
            edgeSet.add((parent[order[i]], order[i]))
            weights = self.getEdgeWeightB(
                lo, hi, trivialProbability)
            edgeLo.append(weights[0])
            edgeHi.append(weights[1])
            edgeActual.append(weights[2])
            costs.append(random.randint(1, n))
        # print(edgeSet)
        m -= (n - 1)
        for i in range(m):
            u, v = random.randint(1, n), random.randint(1, n)
            while u == v or (u, v) in edgeSet:
                u, v = random.randint(1, n), random.randint(1, n)
            edgeFrom.append(u)
            edgeTo.append(v)
            edgeSet.add((u, v))
            edgeSet.add((v, u))
            weights = self.getEdgeWeightB(
                lo, hi, trivialProbability)
            edgeLo.append(weights[0])
            edgeHi.append(weights[1])
            edgeActual.append(weights[2])
            costs.append(random.randint(1, n))
        graph = UncertainGraph()
        graph.buildFromParameters(
            n, edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual, costs)
        return graph

    # All the edges are trivial
    def edgeCaseA(self, n, m, weight):
        return self.costructGraphA(n, m, weight, weight, weight, 0, 1)

    # All the edges are either lo or hi
    def edgeCaseB(self, n, m, lo, hi):
        if lo > hi:
            lo, hi = hi, lo
        if n > 1000 or m < n-1 or m > n*(n - 1)//2:
            assert False
        if lo < 0 or hi < lo:
            assert False
        if lo != hi:
            lo += EPS
            hi -= EPS
        order = [i for i in range(1, n + 1)]
        order = np.array(order)
        random.shuffle(order)
        order = order.tolist()
        parent = [-1 for i in range(n + 1)]
        edgeSet = set()
        for i in range(1, n):
            parent[order[i]] = order[random.randint(0, i-1)]
        edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual = [], [], [], [], []
        for i in range(1, n):
            edgeFrom.append(order[i])
            edgeTo.append(parent[order[i]])
            edgeSet.add((order[i], parent[order[i]]))
            edgeSet.add((parent[order[i]], order[i]))
            edge_lo = random.uniform(lo, hi)
            edge_hi = random.uniform(lo, hi)
            if edge_hi < edge_lo:
                edge_lo, edge_hi = edge_hi, edge_lo
            edgeLo.append(edge_lo)
            edgeHi.append(edge_hi)
            weight = edge_lo + 1e-5
            if random.randint(0, 1):
                weight = edge_hi - 1e-5
            edgeActual.append(weight)
        m -= (n - 1)
        for i in range(m):
            u, v = random.randint(1, n), random.randint(1, n)
            while u == v or (u, v) in edgeSet:
                u, v = random.randint(1, n), random.randint(1, n)
            edgeFrom.append(u)
            edgeTo.append(v)
            edgeSet.add((u, v))
            edgeSet.add((v, u))
            edge_lo = random.uniform(lo, hi)
            edge_hi = random.uniform(lo, hi)
            if edge_hi < edge_lo:
                edge_lo, edge_hi = edge_hi, edge_lo
            edgeLo.append(edge_lo)
            edgeHi.append(edge_hi)
            weight = edge_lo + 1e-5
            if random.randint(0, 1):
                weight = edge_hi - 1e-5
            edgeActual.append(weight)
        graph = UncertainGraph()
        graph.buildFromParameters(
            n, edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual)
        return graph

    # Complete Graph
    def edgeCaseC(self, n, lo, hi, centre=None, deviation=0.5, trivialProbability=0.5):
        return self.costructGraphA(n, n*(n-1)//2, lo, hi, centre, deviation, trivialProbability)


    # All the edges are trivial
    def edgeCase2A(self, n, m, weight):
        return self.costructGraph2A(n, m, weight, weight, weight, 0, 1)

    # All the edges are either lo or hi
    def edgeCase2B(self, n, m, lo, hi):
        if lo > hi:
            lo, hi = hi, lo
        if n > 1000 or m < n-1 or m > n*(n - 1)//2:
            assert False
        if lo < 0 or hi < lo:
            assert False
        if lo != hi:
            lo += EPS
            hi -= EPS
        order = [i for i in range(1, n + 1)]
        order = np.array(order)
        random.shuffle(order)
        order = order.tolist()
        parent = [-1 for i in range(n + 1)]
        edgeSet = set()
        for i in range(1, n):
            parent[order[i]] = order[random.randint(0, i-1)]
        edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual, costs = [], [], [], [], [], []
        for i in range(1, n):
            edgeFrom.append(order[i])
            edgeTo.append(parent[order[i]])
            edgeSet.add((order[i], parent[order[i]]))
            edgeSet.add((parent[order[i]], order[i]))
            edge_lo = random.uniform(lo, hi)
            edge_hi = random.uniform(lo, hi)
            if edge_hi < edge_lo:
                edge_lo, edge_hi = edge_hi, edge_lo
            edgeLo.append(edge_lo)
            edgeHi.append(edge_hi)
            weight = edge_lo + 1e-5
            if random.randint(0, 1):
                weight = edge_hi - 1e-5
            edgeActual.append(weight)
            costs.append(random.randint(1, n))
        m -= (n - 1)
        for i in range(m):
            u, v = random.randint(1, n), random.randint(1, n)
            while u == v or (u, v) in edgeSet:
                u, v = random.randint(1, n), random.randint(1, n)
            edgeFrom.append(u)
            edgeTo.append(v)
            edgeSet.add((u, v))
            edgeSet.add((v, u))
            edge_lo = random.uniform(lo, hi)
            edge_hi = random.uniform(lo, hi)
            if edge_hi < edge_lo:
                edge_lo, edge_hi = edge_hi, edge_lo
            edgeLo.append(edge_lo)
            edgeHi.append(edge_hi)
            weight = edge_lo + 1e-5
            if random.randint(0, 1):
                weight = edge_hi - 1e-5
            edgeActual.append(weight)
            costs.append(random.randint(1, n))
        graph = UncertainGraph()
        graph.buildFromParameters(
            n, edgeFrom, edgeTo, edgeLo, edgeHi, edgeActual, costs)
        return graph

    # Complete Graph
    def edgeCase2C(self, n, lo, hi, centre=None, deviation=0.5, trivialProbability=0.5):
        return self.costructGraph2A(n, n*(n-1)//2, lo, hi, centre, deviation, trivialProbability)