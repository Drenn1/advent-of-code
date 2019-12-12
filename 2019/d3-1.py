GRID_MAX_SIZE = 20000

grid = [x[:] for x in [[0] * GRID_MAX_SIZE] * GRID_MAX_SIZE]

class Point:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

    def __add__(self,o):
        return Point(self.x+o.x, self.y+o.y)

dirs = {
        'U': Point(-1, 0),
        'D': Point(1, 0),
        'L': Point(0, -1),
        'R': Point(0, 1)
        }

def traceGrid(path, byte):
    global grid

    path = [(dirs[s[0]],int(s[1:])) for s in path.split(',')]

    pos = Point()
    for p in path:
        count = p[1]
        while count>0:
            grid[pos.y][pos.x] |= byte
            pos += p[0]
            count-=1

def manDist(a, b):
    return abs(a.x-b.x) + abs(a.y-b.y)

fIn = open('d3.in')
traceGrid(fIn.readline(), 1)
traceGrid(fIn.readline(), 2)

for x in range(-GRID_MAX_SIZE//2, GRID_MAX_SIZE//2):
    for y in range(-GRID_MAX_SIZE//2, GRID_MAX_SIZE//2):
        if grid[y][x] == 3:
            print(str(x) + ', ' + str(y) + ': ' + str(manDist(Point(x, y), Point())))

fIn.close()
