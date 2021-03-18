
from graph import *
from checker import *
from optimal import *
import os

script_dir = os.path.dirname(__file__)

# TESTING for optimal query set
# hand-made cases
print("TESTING ON HAND_MADE CASES...")
for i in range(1, 10):
	rel_path = "tests/test" + str(i) + ".txt"
	abs_file_path = os.path.join(script_dir, rel_path)
	g = UncertainGraph()
	g.buildFromFile(abs_file_path)
	optimalQuerySet(g)
	print("Test " + str(i) + " passed!")


# inputgraph = UncertainGraph()
# inputgraph.buildFromFile(abs_file_path)
# print(inputgraph.edges)
# print(optimalQuerySet(inputgraph))	


# randomly generated cases
testcases = int(input("Enter number of cases to generate and test: "))
for i in range(1, testcases + 1):
	g = UncertainGraph()
	# call generator
	optimalQuerySet(g)
	print("Random test " + str(i) + " passed!")


