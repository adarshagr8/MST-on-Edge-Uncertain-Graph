
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
	optimalSet = optimalQuerySet(g)
	assert checkOPT(g, optimalSet)
	print(len(optimalSet))
	print(optimalSet)
	algoCycleObject = CycleModel(g)
	algoCycleQuery = algoCycleObject.Q
	assert len(algoCycleQuery) <= 2 * len(optimalSet) and checkQuerySet(g, algoCycleQuery)
	print("Test " + str(i) + " passed!")


# inputgraph = UncertainGraph()
# inputgraph.buildFromFile(abs_file_path)
# print(inputgraph.edges)
# print(optimalQuerySet(inputgraph))


# randomly generated cases
testcases = 0
testcases = int(input("Enter number of cases to generate and test: "))
debug = input("Do you want to print generator arguments? [Y/N]: ")
for i in range(1, testcases + 1):
	generatorObject = GraphGenerator(debug == 'Y')
	g = generatorObject.constructGraph(random.randint(12,15), random.randint(15,22), random.uniform(0,100), random.uniform(100,200))
	optimalSet = optimalQuerySet(g)
	assert checkOPT(g, optimalSet)
	# algoCycleObject = CycleModel(g)
	# algoCycleQuery = algoCycleObject.Q
	# assert len(algoCycleQuery) <= 2 * len(optimalSet) and checkQuerySet(algoCycleQuery)
	print("Random test " + str(i) + " passed!")


