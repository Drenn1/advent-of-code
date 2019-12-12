f = open('d1.in', 'r')
lines = f.readlines()
f.close()

fuel = 0
for line in lines:
    fuel += int(line) // 3 - 2

print(fuel)
