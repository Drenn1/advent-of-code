import sys

inF = open('d2.in')
origProgram = [int(x.strip()) for x in inF.read().split(',')]
inF.close()


def run(noun, verb):
    program = origProgram.copy()
    program[1] = noun
    program[2] = verb
    pc = 0
    while True:
        op = program[pc]
        #print('Op ' + str(op) + ' at ' + str(pc))
        if op == 99:
            break
        if op == 1:
            #print('Add ' + str(program[pc+1]) + ' and ' + str(program[pc+2]) + ' to ' + str(program[pc+3]))
            program[program[pc+3]] = program[program[pc+1]] + program[program[pc+2]]
            pc += 4
            continue
        if op == 2:
            program[program[pc+3]] = program[program[pc+1]] * program[program[pc+2]]
            pc += 4
            continue
        print('Unknown opcode ' + str(op))
        exit(1)
    return program[0]


for n in range(0,99):
    for v in range(0,99):
        a = run(n,v)
        if a == 19690720:
            print(str(n) + ',' + str(v))
