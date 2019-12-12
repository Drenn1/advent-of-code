import functools

fIn = open('d4.in')
(start,end) = [int(x) for x in fIn.readline().split('-')]
fIn.close()

count = 0

for x in range(start,end+1):
    chars = str(x).encode()

    def testDouble(l, last=None):
        if len(l) == 0:
            return False
        f, *r = l
        return f == last or testDouble(r, f)

    def testInc(l, last=None):
        if len(l) == 0:
            return True
        f, *r = l
        return (last is None or f >= last) and testInc(r, f)

    if not testDouble(chars) or not testInc(chars):
        continue

    print(x)
    count+=1

print('Total: ' + str(count))
