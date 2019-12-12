import math
import sys

def gcd(x,y):
    x = abs(x)
    y = abs(y)
    if x == 0:
        return y
    if x > y:
        return gcd(y,x)
    return gcd(y%x, x)

f = open('d10.in')
grid = [l.strip() for l in f.readlines()]

HEIGHT = len(grid)
WIDTH = len(grid[0])

asteroids = set([(r,c) for r in range(HEIGHT) for c in range(WIDTH) if grid[r][c] == '#'])


def blocked(r, c, r2, c2):
    assert((r,c) != (r2,c2))
    y = (r2-r) / gcd(r2-r, c2-c)
    x = (c2-c) / gcd(r2-r, c2-c)

    count = 0
    for n in range(1,10000):
        rc = r+y*n
        cc = c+x*n
        if rc == r2 and cc == c2:
            break
        if (r+y*n, c+x*n) in asteroids:
            count+=1
    return count

bestCount = 0
for (r,c) in asteroids:
    count = 0
    for (r2,c2) in asteroids:
        if (r,c) == (r2,c2):
            continue
        if blocked(r, c, r2, c2) == 0:
            count+=1

    if count > bestCount:
        bestPos = (r,c)
        bestCount = max(count, bestCount)

print('Best pos: ' + str(bestPos))
print(bestCount)

(srcR, srcC) = bestPos

def getAngle(r,c):
    assert((r,c) != (srcR,srcC))
    res = -math.atan2(srcC-c,srcR-r)
    if res < 0:
        res += math.pi*2
    res += math.pi*2*blocked(srcR,srcC,r,c)
    return res

asteroids.remove((srcR,srcC))
sortedAsteroids = sorted(asteroids, key=lambda r: getAngle(r[0],r[1]))

print(sortedAsteroids[199])
