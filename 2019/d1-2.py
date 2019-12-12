f = open('d1.in', 'r')
lines = f.readlines()
f.close()

fuel = 0
fuelMegaFinal = 0
for line in lines:
    fuel = int(line) // 3 - 2
    fuelFinal = fuel

    while fuel // 3 - 2 > 0:
        thisfuel = fuel // 3 - 2
        fuelFinal += thisfuel
        fuel = thisfuel

    fuelMegaFinal += fuelFinal

print(fuelMegaFinal)
