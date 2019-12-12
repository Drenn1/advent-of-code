import functools

fIn = open('d4.in')
(start,end) = [int(x) for x in fIn.readline().split('-')]
fIn.close()

count = 0

for x in range(start,end+1):
    chars = str(x).encode()

    def testDouble(l, last=None, lastCount=0):
        if len(l) == 0:
            return lastCount==2
        f, *r = l
        if last == f:
            lastCount+=1
        else:
            if lastCount==2:
                return True
            lastCount=1
        return testDouble(r, f, lastCount)

    def testInc(l, last=None):
        if len(l) == 0:
            return True
        f, *r = l
        return (last is None or f >= last) and testInc(r, f)

    if not testInc(chars):
        continue
#    if not testDouble(chars):
#        continue

    # Alternative iterative check
    reps=0
    lastChar=None
    for c in chars:
        if c == lastChar:
            reps+=1
        else:
            if reps == 2:
                break
            reps=1
        lastChar = c

    if reps != 2:
        continue

    print(x)
    count+=1

print('Total: ' + str(count))
