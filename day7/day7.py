from collections import Counter

inp = open("7").read().splitlines()

start = (0, inp[0].index("S"))
beams = Counter([start])
part1 = 0

for i in range(1, len(inp)):
    temp = Counter()
    for beam in beams:
        if inp[i][beam[1]] == "^":
            temp[(i, beam[1] - 1)] += beams[beam]
            temp[(i, beam[1] + 1)] += beams[beam]
            part1 += 1
        else:
            temp[(i, beam[1])] += beams[beam]
    beams = temp

print(part1)
print(sum(beams.values()))
