f = open('d16.in')
origSignal = [int(x) for x in f.read().strip()]
f.close()


# Part 1
signal = [x for x in origSignal]

for p in range(100):
    newSignal = []
    for o in range(0, len(signal)):
        pattern = sum([[x] * (o+1) for x in [0,1,0,-1]], [])
        index = 1
        v = 0
        for s in signal:
            v += s * pattern[index % len(pattern)]
            index+=1
        newSignal.append(int(str(abs(v))[-1]))

    signal = newSignal

print(signal)


# Part 2
signal = [x for x in origSignal] * 10000
offset = int(''.join(str(x) for x in signal[0:7]))

# Observation: if the offset is >= half the length of the signal, then the
# signal can be computed backwards; the last digit never changes, the 2nd last
# digit is the last signal value + the current signal value for the last digit,
# etc...
# This works because the pattern will be "0" for everything up to the given
# digit, and "1" for everything afterward.
for p in range(0,100):
    newSignal = list([-1] * len(signal))
    for i in reversed(range(offset, len(signal))):
        if i == len(signal)-1:
            newSignal[i] = signal[i]
        else:
            newSignal[i] = signal[i] + newSignal[i+1]
    signal = [x % 10 for x in newSignal]

print(signal[offset:offset+8])
