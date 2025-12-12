inp = open("12").read().splitlines()
blocks = [
    sum(map(lambda x: sum(map(lambda x: x == "#", list(x))), inp[i + 1 : i + 4]))
    for i in range(0, 30, 5)
]
problems = [
    (tuple(map(int, i[:5].split("x"))), list(map(int, i[7:].split()))) for i in inp[30:]
]

part1 = 0
for problem in problems:
    total = 0
    for i in range(6):
        total += problem[1][i]

    part1 += 1 if (problem[0][0] // 3) * (problem[0][1] // 3) >= total else 0

print(part1)
