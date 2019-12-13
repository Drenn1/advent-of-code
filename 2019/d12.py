import copy
import math

class Moon:
    def __init__(self, s):
        s = s.strip()[1:][:-1].split(',')
        self.pos = [0,0,0]
        self.vel = [0,0,0]
        self.pos[0] = int(s[0].split('=')[1])
        self.pos[1] = int(s[1].split('=')[1])
        self.pos[2] = int(s[2].split('=')[1])

    def __repr__(self):
        return str(tuple(self.pos))

    def pot(self):
        return sum([abs(x) for x in self.pos])

    def kin(self):
        return sum([abs(x) for x in self.vel])

    def tot(self):
        return self.pot() * self.kin()


f = open('d12.in')
origMoons = [Moon(x) for x in f.readlines()]
f.close()


# Run 1 step of the moon simulation
def nextStep():
    oldmoons = copy.deepcopy(moons)
    for i,m in enumerate(moons):
        for j,n in enumerate(oldmoons):
            if i == j:
                continue
            for a in range(3):
                if m.pos[a] < n.pos[a]:
                    m.vel[a]+=1
                elif m.pos[a] > n.pos[a]:
                    m.vel[a]-=1

        m.pos = [sum(x) for x in zip(m.pos, m.vel)]
        assert(len(m.pos) == 3)

    return 1


INFINITY = 10000000000

# This function is completely unnecessary for my solution, but I worked hard on
# it, so I'm keeping it.
# It's supposed to run multiple steps at a time by detecting how many steps it
# will be until acceleration values change, though it doesn't quite work.
# This isn't helpful anyway because the X/Y/Z values are so close together.
def efficientSteps():
    oldmoons = copy.deepcopy(moons)

    # Get acceleration of moon m caused by moon n on given axis
    def accVal(m, n, axis):
        if m.pos[axis] < n.pos[axis]:
            return 1
        elif m.pos[axis] > n.pos[axis]:
            return -1
        else:
            return 0

    # Get total acceleration of moon m on given axis
    def totalAcc(m, axis):
        return sum(accVal(m, x, axis) for x in oldmoons if x != m)

    # Return the number of steps until moon m will pass moon n on the given axis
    def timeToOvertake(m, n, axis):
        if m.pos[axis] > n.pos[axis]:
            (m,n) = (n,m) # We make assumptions about their relative positions (I think?)
        mp = m.pos[axis]
        np = n.pos[axis]
        mvi = m.vel[axis]
        nvi = n.vel[axis]
        acc = totalAcc(m, axis) - totalAcc(n, axis)
        vi = mvi - nvi + acc*0.5 # Hack to deal with acceleration applying before movement change
        root = vi*vi - 2*acc*(mp - np)
        if root < 0:
            return INFINITY
        if acc == 0:
            if vi == 0:
                return INFINITY
            return (mp - np) / vi
        val1 = (-vi + root**0.5) / acc
        val2 = (-vi - root**0.5) / acc
        if val2 > 0:
            return val2 # Return smallest higher than 0
        if val1 <= 0:
            return INFINITY
        return val1

    #print(timeToOvertake(moons[0], moons[1], 0))
    numSteps = [timeToOvertake(m, n, axis) for m in moons for n in moons for axis in range(0,3) if m != n]
    numSteps = math.ceil(min([x for x in numSteps if x != 0]))
    assert(numSteps >= 1)

    for m in moons:
        for axis in range(0,3):
            acc = totalAcc(m, axis)
            vi = m.vel[axis] + acc*0.5
            m.pos[axis] += vi*numSteps + acc*0.5*numSteps*numSteps
            m.vel[axis] += acc*numSteps
            assert(m.pos[axis] == int(m.pos[axis]))
            assert(m.vel[axis] == int(m.vel[axis]))
            m.pos[axis] = int(m.pos[axis])
            m.vel[axis] = int(m.vel[axis])

    return numSteps


print('--------------------')
print('PART 1')
print('--------------------')

moons = copy.deepcopy(origMoons)
steps = 0
while steps < 1000:
    numSteps = nextStep()
    steps += numSteps

print('Total energy after ' + str(steps) + ' steps: ' + str(sum([x.tot() for x in moons])))
print('Moon states: ' + str(moons))



print('--------------------')
print('PART 2')
print('--------------------')

def cycleLen(axis):
    global moons

    moons = copy.deepcopy(origMoons)
    steps = 0
    visited = set()
    while True:
        key = tuple((m.pos[axis], m.vel[axis]) for m in moons)
        if key in visited:
            break
        visited.add(key)
        steps+=nextStep()
    return steps


xCycle = cycleLen(0)
yCycle = cycleLen(1)
zCycle = cycleLen(2)

print('X Cycle Len: ' + str(xCycle))
print('Y Cycle Len: ' + str(yCycle))
print('Z Cycle Len: ' + str(zCycle))

# Too lazy to write LCM algorithm, use an online calculator
