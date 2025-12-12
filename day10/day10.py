from collections import deque
from z3 import Int, Optimize, Sum, sat

inp = list(map(str.split, open("10").read().splitlines()))

data = []
for line in inp:
    temp = []
    temp.append(sum(1 << i for i, v in enumerate(line[0][1:-1]) if v == "#"))
    temp += list(map(lambda x: tuple(map(int, x[1:-1].split(","))), line[1:-1]))
    temp.append(tuple(map(int, line[-1][1:-1].split(","))))

    data.append(tuple(temp))

part1 = 0
for line in data:
    goal = line[0]
    q = deque([(i, 0, 0) for i in line[1:-1]])
    visited = set()
    while (curr := q.popleft())[1] != goal:
        new = curr[1]
        switch = 0
        for i in curr[0]:
            switch += 1 << i
        new ^= switch

        if new in visited:
            continue
        visited.add(new)

        q.extend([(i, new, curr[2] + 1) for i in line[1:-1]])
    part1 += curr[2]

print(f"Part 1: {part1}")

part2 = 0

for line in data:
    ints = []

    s = Optimize()

    for i in range(len(line[1:-1])):
        ints.append(Int(f"v{i}"))
        s.add(ints[i] >= 0)

    for i in range(len(line[-1])):
        x = []
        for j in range(len(line[1:-1])):
            if i in line[j + 1]:
                x.append(ints[j])

        s.add(Sum(x) == line[-1][i])

    s.minimize(Sum(ints))

    if s.check() == sat:
        m = s.model()
        part2 += m.evaluate(Sum(ints)).as_long()
print(f"Part 2: {part2}")
