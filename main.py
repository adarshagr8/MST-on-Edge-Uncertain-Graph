from graph import *
from checker import *
from weightedOptimal import *
from weightedAlgoCycle import *
from generator import *
# from algoCycle import *
# from algoCut import *
import random
import os

script_dir = os.path.dirname(__file__)

def CompetitiveRatio(a, b):
    if b == 0:
        assert a == 0
        return 1.0
    else:
        return a/b

def runLargeTest(fileName):
    print("Running on large network: " + fileName)
    rel_path = "tests/" + fileName
    abs_file_path = os.path.join(script_dir, rel_path)
    g = UncertainGraph()
    g.buildFromFile(abs_file_path)
    print(g)
    optimalSet = weightedOptimalQuerySet(g)
    # assert checkOPT(g, optimalSet)
    # print(len(optimalSet))
    # print(optimal Set)
    algoCycleObject = CycleModel(g)
    algoCycleQuery = algoCycleObject.Q
    print(len(algoCycleQuery), len(optimalSet))
    print("Algo Cycle Competitve Ratio:", CompetitiveRatio(getTotalQueryCost(
        algoCycleQuery), getTotalQueryCost(optimalSet)))
    assert getTotalQueryCost(algoCycleQuery) <= 2 * getTotalQueryCost(optimalSet)
    assert checkQuerySet(g, algoCycleQuery)
    print("Test Passed!")


# TESTING for optimal query set
# hand-made cases
print("TESTING ON HAND-MADE CASES...")
for i in range(1, 10):
    rel_path = "tests/test" + str(i) + ".txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    g = UncertainGraph()
    g.buildFromFile(abs_file_path)

    optimalSet = weightedOptimalQuerySet(g)
    assert checkOPT(g, optimalSet)
    # print(len(optimalSet))
    # print(optimal Set)
    algoCycleObject = CycleModel(g)
    algoCycleQuery = algoCycleObject.Q
    print("Algo Cycle Competitve Ratio:", CompetitiveRatio(getTotalQueryCost(
        algoCycleQuery), getTotalQueryCost(optimalSet)))
    # print(len(algoCutQuery), len(optimalSet))
    assert getTotalQueryCost(algoCycleQuery) <= 2 * getTotalQueryCost(optimalSet)
    assert checkQuerySet(g, algoCycleQuery)
    print("Test " + str(i) + " passed!")


for i in [4, 10, 100, 200, 500, 1000]:
    runLargeTest("USA" + str(i) + ".gr")


# randomly generated cases
testcases = 0
testcases = int(input("Enter number of cases to generate and test: "))
debug = input("Do you want to print generator arguments? [Y/N]: ")
totalCycleSet = 0
totalCutSet = 0
totalOptSet = 0
for i in range(1, testcases + 1):
    generatorObject = GraphGenerator(debug == 'Y')
    if random.randint(0, 1):
        g = generatorObject.constructGraph2B(
            100, 200, random.uniform(0, 100), random.uniform(100, 200))
    else:
        g = generatorObject.constructGraph2A(
            100, 200, random.uniform(0, 100), random.uniform(100, 200))
    # print(g)
    optimalSet = weightedOptimalQuerySet(g)
    # assert checkOPT(g, optimalSet)
    algoCycleObject = CycleModel(g)
    algoCycleQuery = algoCycleObject.Q
    print("Algo Cycle Competitve Ratio:", CompetitiveRatio(getTotalQueryCost(
        algoCycleQuery), getTotalQueryCost(optimalSet)))
    totalCycleSet += getTotalQueryCost(algoCycleQuery)
    totalOptSet += getTotalQueryCost(optimalSet)
    assert getTotalQueryCost(algoCycleQuery) <= 2 * getTotalQueryCost(optimalSet)
    assert checkQuerySet(g, algoCycleQuery)
    print("Random test " + str(i) + " passed!")

print("Average Algo Cycle Competitve Ratio:",
      CompetitiveRatio(totalCycleSet, totalOptSet))
print("Average Algo Cut Competitve Ratio:",
      CompetitiveRatio(totalCutSet, totalOptSet))

