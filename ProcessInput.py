from numpy import random
f = open("USARoadDataSet.gr", "r+")
newContent = []
for line in f:
    prob = random.uniform(0, 1)
    u, v, actual = map(int, line.split())
    lo = random.randint(0, actual)
    hi = random.randint(actual + 1, actual + random.randint(500, 1000))
    if prob < 0.1:
        line = str(u) + ' ' + str(v) + ' ' + str(actual) + ' ' + str(actual) + ' ' + str(actual)
    else:
        line = str(u) + ' ' + str(v) + ' ' + str(lo) + ' ' + str(hi) + ' ' + str(actual)
    newContent.append(line)
f.seek(0)
f.write('\n'.join(newContent))
f.close()