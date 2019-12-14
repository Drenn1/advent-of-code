import math
from collections import defaultdict

class Reaction:
    def __init__(self, s):
        def parsePair(s):
            s = s.strip().split(' ')
            return (s[1].strip(), int(s[0]))

        self.input = [parsePair(x) for x in s.split('=>')[0].split(',')]
        self.output = parsePair(s.split('=>')[1])

    def __repr__(self):
        return str((self.input, self.output))


f = open('d14.in')
reactions = [Reaction(x) for x in f.readlines()]
f.close()

outputDict = dict((x.output[0], x) for x in reactions)

def produce(chem, quant):
    leftovers = defaultdict(lambda: 0)

    def produceHelper(chem, quant):
        if chem == 'ORE':
            return quant

        leftoversUsed = min(leftovers[chem], quant)
        quant -= leftoversUsed
        leftovers[chem] -= leftoversUsed

        reaction = outputDict[chem]
        inMult = math.ceil(quant / reaction.output[1])

        leftovers[chem] += inMult * reaction.output[1] - quant

        total = 0
        for inp in reaction.input:
            total += produceHelper(inp[0], inp[1] * inMult)
        return total

    return produceHelper(chem, quant)



print('-------PART 1-------')
print('ORE required: ' + str(produce('FUEL', 1)))


print('\n-------PART 2-------')

def binsearch(l, h, target):
    m = (l+h+1)//2
    val = produce('FUEL', m)
    if l == h:
        return m
    elif target > val:
        return binsearch(m, h, target)
    elif target < val:
        return binsearch(l, m-1, target)
    else:
        return m

fuelAmount = binsearch(0, 100000000, 1000000000000)
print(str(fuelAmount) + ' fuel takes ' + str(produce('FUEL', fuelAmount)) + ' ore')
