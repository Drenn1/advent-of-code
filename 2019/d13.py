import curses
import intcode
import time

GRID_SIZE = 50
gridCharDict = {0: ' ', 1: '#', 2: 'O', 3: '_', 4: '.'}

grid = [x[:] for x in [[0] * GRID_SIZE] * GRID_SIZE]

outputIndex = 0
stdscr = None

def outputFunc(val):
    global outputIndex, outputX, outputY, finalScore, paddlePos, ballPos
    if outputIndex == 0:
        outputX = val
        outputIndex+=1
    elif outputIndex == 1:
        outputY = val
        outputIndex+=1
    else:
        outputIndex = 0
        if outputX == -1 and outputY == 0:
            finalScore = val
            return
        assert(outputY < GRID_SIZE and outputY >= 0)
        assert(outputX < GRID_SIZE and outputX >= 0)
        if val == 3:
            paddlePos = outputX
        elif val == 4:
            ballPos = outputX
        grid[outputY][outputX] = val
        if stdscr is not None: # ncurses display
            stdscr.addch(outputY, outputX, gridCharDict[val])

def printGrid():
    for y in range(GRID_SIZE):
        print(''.join([gridCharDict[x] for x in grid[y]]))



print('-------PART 1-------\n')
program = intcode.fromFile('d13.in')
program.run(None, outputFunc)
print('Num blocks: ' + str(len([x for x in sum(grid, []) if x == 2])))
printGrid()


print('-------PART 2-------\n')

def inputFunc():
    if paddlePos < ballPos:
        return 1
    elif paddlePos > ballPos:
        return -1
    else:
        return 0

program = intcode.fromFile('d13.in')
program.memory[0] = 2 # Insert quarters

# Just for fun, show the game in real-time
try:
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.clear()
    while True:
        for i in range(3):
            output = program.run(inputFunc, outputFunc, returnOutput=True)
        if output is None:
            break
        stdscr.refresh()
        time.sleep(0.001)

finally:
    curses.echo()
    curses.endwin()

print('Final Score: ' + str(finalScore))
