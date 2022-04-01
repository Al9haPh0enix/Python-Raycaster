import random


with open("world.wor", "w") as f:
    for y in range(8):
        for x in range(8):
            n = random.choice([0, 0, 0, 0, 1])
            if y == 0 or y == 7:
                n = 1
            if x == 0 or x == 7:
                n = 1
            f.write(str(n) + " ")
        f.write("\n")