import copy

WIDTH = 25
HEIGHT = 6

def splitArray(a, l):
    out = []
    assert(len(a) % l == 0)
    for i in range(len(a)//l):
        out.append(a[i*l:(i+1)*l])
    return out

def countValue(a, v):
    return len([x for x in a if x == v])

def countLayerValue(layer, v):
    return sum([countValue(x, v) for x in layer])

def genImage(layers):
    grid = copy.deepcopy(layers[-1])
    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        grid[y] = list(grid[y])

    for l in reversed(layers):
        for y in range(height):
            for x in range(width):
                c = l[y][x]
                if c == '2':
                    continue
                grid[y][x] = c
    return grid

def convChar(c):
    if c == '0':
        return ' '
    if c == '1':
        return '#'
    return c

def drawImage(grid):
    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        print(''.join([convChar(x) for x in grid[y]]))

fIn = open('d8.in')
array = [splitArray(x, WIDTH) for x in splitArray(fIn.read().strip(), WIDTH*HEIGHT)]
fIn.close()

index = min(range(len(array)), key=lambda x:countLayerValue(array[x], '0'))
layer = array[index]

print(countLayerValue(layer, '1') * countLayerValue(layer, '2'))
drawImage(genImage(array))
