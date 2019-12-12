import intcode

GRID_SIZE = 100

grid = [x.copy() for x in [['.'] * GRID_SIZE] * GRID_SIZE]
painted = set()

(r,c) = (GRID_SIZE//2, GRID_SIZE//2)
facing = 0

facingTable = [
        (-1,0),
        (0,1),
        (1,0),
        (0,-1)]

grid[r][c] = '#'

f = open('d11.in')
program = intcode.Intcode([int(x.strip()) for x in f.read().split(',')])
f.close()

def inputFunc():
    return 0 if grid[r][c] == '.' else 1

paintedCount = 0
while True:
    colorOutput = program.run(inputFunc, None, returnOutput=True)

    if colorOutput is None:
        break
    if not (r,c) in painted:
        paintedCount+=1
    painted.add((r,c))

    grid[r][c] = '.' if colorOutput == 0 else '#'

    turnOutput = program.run(inputFunc, None, returnOutput=True)

    if turnOutput == 0:
        facing-=1
    elif turnOutput == 1:
        facing+=1
    else:
        assert(False)
    facing %= 4

    r += facingTable[facing][0]
    c += facingTable[facing][1]

def drawGrid():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            print(grid[r][c], end='')
        print()

print(paintedCount)
drawGrid()
