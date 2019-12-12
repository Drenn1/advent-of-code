import sys

inF = open('d2.in')
program = [int(x.strip()) for x in inF.read().split(',')]
inF.close()


program[1] = 12
program[2] = 2

pc = 0

print(program)

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

print('Output: ' + str(program[0]))
