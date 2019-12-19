import itertools
import intcode

#f = open('d17.in')
#grid = [list(x.strip()) for x in f.readlines()]
#f.close()

origProgram = intcode.fromFile('d17.in')
program = origProgram.copy()

grid = []
program.run(None, lambda c: grid.append(c))
grid = [list(x) for x in ''.join([chr(c) for c in grid]).strip().split('\n')]

ROWS = len(grid)
COLS = len(grid[0])

botDirections = {
        '<': [0,-1],
        '>': [0, 1],
        '^': [-1, 0],
        'v': [1, 0]
        }

def getPoints():
    return itertools.product(range(ROWS), range(COLS))


# Search for bot position
for r,c in getPoints():
    if grid[r][c] in botDirections.keys():
        #grid[r][c] = '#'
        print('Bot position: ' + str((r,c)))


def isIntersection(r,c):
    if r == 0 or r == ROWS-1 or c == 0 or c == COLS-1:
        return False
    return grid[r][c] == '#' \
            and grid[r][c+1] == '#' \
            and grid[r][c-1] == '#' \
            and grid[r+1][c] == '#' \
            and grid[r-1][c] == '#'

def getIntersections():
    for r,c in getPoints():
        if isIntersection(r,c):
            yield (r,c)

def printGrid():
    for r in grid:
        print(''.join(r))


print('------PART 1------')
print(sum([r * c for r,c in getIntersections()]))
#printGrid()


print('------PART 2------')

# Part 2

# I worked out this movement pattern manually (sue me):
#
# A: L,10,R,8,R,6,R,10,
# B: L,12,R,8,L,12,
# A: L,10,R,8,R,6,R,10,
# B: L,12,R,8,L,12,
# C: L,10,R,8,R,8,
# C: L,10,R,8,R,8,
# B: L,12,R,8,L,12,
# A: L,10,R,8,R,6,R,10,
# C: L,10,R,8,R,8,
# A: L,10,R,8,R,6,R,10


routines = ['A,B,A,B,C,C,B,A,C,A',
        'L,10,R,8,R,6,R,10',
        'L,12,R,8,L,12',
        'L,10,R,8,R,8',
        'n']


routineIndex = 0
routineOffset = 0

def inputFunc():
    global routineIndex, routineOffset
    if len(routines[routineIndex]) == routineOffset:
        routineIndex+=1
        routineOffset=0
        return ord('\n')
    routineOffset+=1
    return ord(routines[routineIndex][routineOffset-1])

def outputFunc(o):
    global lastOutputBuffer
    if o < 256:
        print(chr(o), end='')
    else:
        print(o)

program = origProgram.copy()
program.memory[0] = 2
program.run(inputFunc, outputFunc)
