
from graph import *
from checker import *
from optimal import *
from generator import *
from algoCycle import *
import random
import os

script_dir = os.path.dirname(__file__)

# TESTING for optimal query set
# hand-made cases
print("TESTING ON HAND-MADE CASES...")
for i in range(1, 8):
	rel_path = "tests/test" + str(i) + ".txt"
	abs_file_path = os.path.join(script_dir, rel_path)
	g = UncertainGraph()
	g.buildFromFile(abs_file_path)
	print(g)
	assert checkOPT(g, optimalQuerySet(g))
	print(len(optimalQuerySet(g)))
	print(optimalQuerySet(g))
	# algoCycleObject = CycleModel(g)
	# algoCycleQuery = algoCycleObject.Q
	# assert len(algoCycleQuery) <= 2 * len(optimalSet) and checkQuerySet(algoCycleQuery)
	print("Test " + str(i) + " passed!")


# inputgraph = UncertainGraph()
# inputgraph.buildFromFile(abs_file_path)
# print(inputgraph.edges)
# print(optimalQuerySet(inputgraph))


# randomly generated cases
testcases = 0
# testcases = int(input("Enter number of cases to generate and test: "))
for i in range(1, testcases + 1):
	generatorObject = GraphGenerator()
	g = costructGraph(random.randint(10,20), random.randint(20,30), random.uniform(0,100), random.uniform(100,200))
	optimalSet = optimalQuerySet(g)
	assert checkOPT(g, optimalSet)
	# algoCycleObject = CycleModel(g)
	# algoCycleQuery = algoCycleObject.Q
	# assert len(algoCycleQuery) <= 2 * len(optimalSet) and checkQuerySet(algoCycleQuery)
	print("Random test " + str(i) + " passed!")


