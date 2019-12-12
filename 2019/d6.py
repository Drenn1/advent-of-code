import sys
import functools
import operator
import collections

sys.setrecursionlimit(10000)

f = open('d6.in')
orbitsList = [s.strip().split(')') for s in f.readlines()]
f.close()

nodes = set(functools.reduce(operator.iconcat, orbitsList, []))

orbitsDict = {}                     # Forward edges
edges = dict((x,[]) for x in nodes) # Undirected edges

for n in nodes:
    orbitsDict[n] = list(map(lambda x:x[1], filter(lambda x:x[0]==n, orbitsList)))
for o in orbitsList:
    edges[o[0]].append(o[1])
    edges[o[1]].append(o[0])

# Count number of orbits below this object
def traverse(n, depth=1):
    return len(orbitsDict[n]) * depth + sum(traverse(x,depth+1) for x in orbitsDict[n])

def bfs(src, dest):
    visited = set()
    toVisit = collections.deque([(src,0)])
    while len(toVisit) > 0:
        n,depth = toVisit.popleft()
        if n in visited:
            continue
        visited.add(n)
        if n == dest:
            return depth
        toVisit.extend((e, depth+1) for e in edges[n])

    return -1

# Subproblem 1
print(traverse('COM'))

# Subproblem 2
print(bfs('YOU', 'SAN') - 2)
