INFINITY = 99999999

gridA = {}
gridB = {}

class Point:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def __add__(self,o):
        return Point(self.x+o.x, self.y+o.y)

    def __eq__(self,o):
        return self.x==o.x and self.y==o.y

    def __hash__(self):
        return (self.x<<20)+self.y

dirs = {
        'U': Point(-1, 0),
        'D': Point(1, 0),
        'L': Point(0, -1),
        'R': Point(0, 1)
        }

def traceGrid(path, grid):
    tracedPoints = set()
    path = [(dirs[s[0]],int(s[1:])) for s in path.split(',')]

    pos = Point()
    steps = 0
    for p in path:
        count = p[1]
        while count>0:
            grid[pos] = min(grid.get(pos, INFINITY), steps)
            tracedPoints.add(pos)

            pos += p[0]

            count-=1
            steps += 1
    return tracedPoints

def manDist(a, b):
    return abs(a.x-b.x) + abs(a.y-b.y)

fIn = open('d3.in')
pointsA = traceGrid(fIn.readline(), gridA)
pointsB = traceGrid(fIn.readline(), gridB)

for p in pointsA.intersection(pointsB):
    s1 = gridA[p]
    s2 = gridB[p]
    print(str(s1) + ' + ' + str(s2) + ' = ' + str(s1+s2))

fIn.close()
