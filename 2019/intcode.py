# "Intcode" simulator + solutions for days 5, 7, 9.
# Days 11+ import this file since the simulator was completed in day 9.

import sys
import itertools
import functools

sys.setrecursionlimit(100000)

opAliases = [
        0,
        'ADD',
        'MUL',
        'INP',
        'OUT',
        'JIT',
        'JIF',
        'LTN',
        'EQL',
        'REL'
        ]

paramCounts = [ 0, 3, 3, 1, 1, 2, 2, 3, 3, 1 ]

# Amount of memory to 0-initialize
MEM_SIZE = 10000

class Intcode:
    def __init__(self,program):
        self.program = program.copy()
        self.pc = 0
        self.relbase = 0

        if len(self.program) < MEM_SIZE:
            self.program.extend([0] * (MEM_SIZE - len(self.program)))

    def copy(self):
        p = Intcode(self.program)
        p.pc = self.pc
        p.relbase = self.relbase
        return p

    # Normally runs until termination, but if "returnOutput"==True, this returns
    # when output is sent.
    def run(self, inputFunc, outputFunc, returnOutput=False, debug=False):
        program = self.program

        def readParamPosition(offset):
            return program[program[self.pc + offset]]
        def readParamImmediate(offset):
            return program[self.pc + offset]
        def readParamRelative(offset):
            return program[program[self.pc + offset] + self.relbase]

        def writeParamPosition(offset, val):
            program[program[self.pc + offset]] = val
        def writeParamRelative(offset, val):
            program[program[self.pc + offset] + self.relbase] = val

        readParamTable = [readParamPosition, readParamImmediate, readParamRelative]
        writeParamTable = [writeParamPosition, 0, writeParamRelative]

        def readParam(offset):
            return readParamTable[int(paramModeString[-offset])](offset)

        def writeParam(offset, val):
            writeParamTable[int(paramModeString[-offset])](offset, val)

        def printOpInfo(op):
            sys.stdout.write(str(self.pc) + ': ')
            if op == 99:
                print('END')
                return
            sys.stdout.write(opAliases[op])
            for i in range(paramCounts[op]):
                b = program[self.pc+i+1]
                if paramModeString[-i] == 0:
                    sys.stdout.write(' [' + str(b)  + ']')
                elif paramModeString[-i] == 1:
                    sys.stdout.write(' ' + str(b))
                else:
                    sys.stdout.write(' [' + str(b) + ' + ' + str(self.relbase) + ']')
            print()


        while True:
            paramModeString = str(program[self.pc])[:-2]
            while len(paramModeString) < 3:
                paramModeString = '0' + paramModeString

            op = int(str(program[self.pc])[-2:])

            if debug:
                printOpInfo(op)

            # Init again after printOpInfo
            paramModeString = str(program[self.pc])[:-2]
            while len(paramModeString) < 3:
                paramModeString = '0' + paramModeString

            if op == 99: # END
                break
            elif op == 1: # ADD
                writeParam(3, readParam(1) + readParam(2))
            elif op == 2: # MUL
                writeParam(3, readParam(1) * readParam(2))
            elif op == 3: # INP
                writeParam(1, inputFunc())
            elif op == 4: # OUT
                outVal = readParam(1)
                if outputFunc is not None:
                    outputFunc(outVal)
                if returnOutput == True:
                    self.pc += paramCounts[op] + 1
                    return outVal
            elif op == 5: # JIT
                if readParam(1) != 0:
                    self.pc = readParam(2)
                    continue
            elif op == 6: # JIF
                if readParam(1) == 0:
                    self.pc = readParam(2)
                    continue
            elif op == 7: # LTN
                if readParam(1) < readParam(2):
                    writeParam(3, 1)
                else:
                    writeParam(3, 0)
            elif op == 8: # EQL
                if readParam(1) == readParam(2):
                    writeParam(3, 1)
                else:
                    writeParam(3, 0)
            elif op == 9: # REL
                self.relbase += readParam(1)
            else:
                print('Unknown opcode ' + str(op))
                exit(1)

            # NOTE: not all opcodes reach here
            self.pc += paramCounts[op] + 1
            continue

        return None


def prepProblem(prob, subprob, expected=None):
    global origIntcode
    inF = open('d' + str(prob) + '.in')
    origIntcode = [int(x.strip()) for x in inF.read().split(',')]
    inF.close()
    print('\n-----------------')
    print('PROBLEM ' + str(prob) + '-' + str(subprob))
    if expected is not None:
        print('EXPECTED OUTPUT: ' + str(expected))
    print('-----------------')

def defaultOutputFunc(v):
    print('OUTPUT: ' + str(v))


if __name__ == "__main__":
    if 1: # Day 5
        prepProblem(5, 1, 16434972)
        p = Intcode(origIntcode)
        p.run(lambda: 1, defaultOutputFunc, debug=False)

        prepProblem(5, 2, 16694270)
        p = Intcode(origIntcode)
        p.run(lambda: 5, defaultOutputFunc, debug=False)


    if 1: # Day 7-1
        prepProblem(7, 1, 914828)

        bestOutput = 0
        for perm in itertools.permutations([0,1,2,3,4]):
            lastOutputFunction = lambda: 0
            gotPhaseList = [False] * len(perm)

            def inputFunc(phase, inFunc):
                if gotPhaseList[phase]:
                    return inFunc()
                else:
                    gotPhaseList[phase] = True
                    return phase

            for i in range(len(perm)):
                p = Intcode(origIntcode)
                finalInput = functools.partial(inputFunc, perm[i], lastOutputFunction)
                lastOutputFunction = functools.partial(p.run, finalInput, None, returnOutput=True)

            output = lastOutputFunction()
            bestOutput = max(bestOutput, output)

        print(bestOutput)


    if 1: # Day 7-2
        prepProblem(7, 2, 17956613)

        bestOutput = 0
        for perm in itertools.permutations([5,6,7,8,9]):
            programs = [x.copy() for x in [Intcode(origIntcode)] * len(perm)]
            gotPhaseList = [False] * len(perm)
            gotInitialInput = False

            finalOutputValue = None
            prevOutputFunction = lambda: finalOutputValue

            def inputFunc(index, inFunc):
                global gotInitialInput
                if not gotPhaseList[index]:
                    gotPhaseList[index] = True
                    return perm[index]
                elif index == 0 and not gotInitialInput:
                    gotInitialInput = True
                    return 0
                if gotPhaseList[index]:
                    return inFunc()

            for i in range(len(perm)):
                finalInput = functools.partial(inputFunc, i, prevOutputFunction)
                prevOutputFunction = functools.partial(programs[i].run, finalInput, None, returnOutput=True)

            while True:
                output = finalOutputValue
                finalOutputValue = prevOutputFunction()
                if finalOutputValue == None:
                    break

            bestOutput = max(bestOutput, output)

        print(bestOutput)


    if 1: # Day 9
        prepProblem(9, 1, 3598076521)
        p = Intcode(origIntcode)
        p.run(lambda: 1, defaultOutputFunc)

        prepProblem(9, 2, 90722)
        p = Intcode(origIntcode)
        p.run(lambda: 2, defaultOutputFunc)
