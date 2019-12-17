import intcode
import curses
import collections

GRID_SIZE = 50

program = intcode.fromFile('d15.in')

directionTable = [
        [],
        [-1,0],
        [1,0],
        [0,-1],
        [0,1]]

directionInvert = [-1, 2, 1, 4, 3]

charLookup = {0: '#', 1: '.', 2: 'O'}

# Interactive mode, just for fun
def exploreWithNcurses():
    grid = [x[:] for x in [[-1] * GRID_SIZE] * GRID_SIZE]

    droidX = GRID_SIZE//2
    droidY = GRID_SIZE//2

    try:
        stdscr = curses.initscr()
        curses.noecho()
        stdscr.keypad(True)

        stdscr.clear()
        stdscr.addch(droidY, droidX, 'D')

        grid[droidY][droidX] = '.'

        while True:
            k = stdscr.getch()
            if k == curses.KEY_UP:
                inputVal = 1
            elif k == curses.KEY_DOWN:
                inputVal = 2
            elif k == curses.KEY_LEFT:
                inputVal = 3
            elif k == curses.KEY_RIGHT:
                inputVal = 4
            else:
                continue

            output = program.run(lambda: inputVal, None, returnOutput=True)

            gridY = droidY + directionTable[inputVal][0]
            gridX = droidX + directionTable[inputVal][1]
            if output == 0:
                gridChar = '#'
            elif output == 1 or output == 2:
                stdscr.addch(droidY, droidX, grid[droidY][droidX])
                droidY = gridY
                droidX = gridX
                if output == 1:
                    gridChar = '.'
                else:
                    gridChar = 'O'
            else:
                assert(False)

            grid[gridY][gridX] = gridChar
            if gridChar == '.':
                stdscr.addch(gridY, gridX, 'D')
            else:
                stdscr.addch(gridY, gridX, gridChar)
            stdscr.refresh()

    finally:
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

#exploreWithNcurses()


# Actual solution starts here

startR = GRID_SIZE//2
startC = GRID_SIZE//2
grid = [x[:] for x in [[' '] * GRID_SIZE] * GRID_SIZE]
grid[startR][startC] = 'S'


# Traverses the entire grid to get the full picture
def traverseGrid(r, c, d):
    global grid
    global oxygenR, oxygenC

    if grid[r][c] == 'O':
        oxygenR = r
        oxygenC = c

    for i in range(1,5):
        r2 = r + directionTable[i][0]
        c2 = c + directionTable[i][1]
        if grid[r2][c2] != ' ':
            continue
        val = charLookup[program.run(lambda: i, None, returnOutput=True)]
        grid[r2][c2] = val
        if val != '#':
            traverseGrid(r2, c2, i)

    if d != -1:
        program.run(lambda: directionInvert[d], None, returnOutput=True)


def printGrid():
    for r in range(GRID_SIZE):
        print(''.join(grid[r]))


# Part 1 searches for 'O' from start position.
# Part 2 exhausts entire grid from oxygen position.
def bfs(startR, startC, targetChar):
    visited = set()
    
    queue = collections.deque()
    queue.append((startR,startC,0))
    maxdepth = 0

    while len(queue) != 0:
        (r,c,d) = queue.popleft()
        if (r,c) in visited:
            continue
        if grid[r][c] == '#':
            continue
        if grid[r][c] == targetChar:
            return d
        maxdepth = max(d,maxdepth)
        visited.add((r,c))

        for i in range(1,5):
            r2 = r + directionTable[i][0]
            c2 = c + directionTable[i][1]
            queue.append((r2,c2,d+1))

    return maxdepth


traverseGrid(startR, startC, -1)
printGrid()

# Part 1
print('Shortest path to O: ' + str(bfs(startR, startC, 'O')))

# Part 2
print('Time to fill oxygen: ' + str(bfs(oxygenR, oxygenC, '\0')))
