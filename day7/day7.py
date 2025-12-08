from collections import Counter

inp = open("7").read().splitlines()

beams = Counter([inp[0].index("S")])
part1 = 0

for i in range(1, len(inp)):
    temp = Counter()
    for beam in beams:
        if inp[i][beam] == "^":
            temp[beam - 1] += beams[beam]
            temp[beam + 1] += beams[beam]
            part1 += 1
        else:
            temp[beam] += beams[beam]
    beams = temp

print(part1)
print(sum(beams.values()))
