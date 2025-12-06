inp = open("5").read().splitlines()
ranges = [list(map(int, i.split("-"))) for i in inp[: inp.index("")]]
ids = map(int, inp[inp.index("") + 1 :])

total = 0
for i in ids:
    for r in ranges:
        if r[0] <= i <= r[1]:
            total += 1
            break

print(f"part 1: {total}")

ranges.sort(key=lambda x: x[0])

i = 0
while i < len(ranges) - 1:
    curr = ranges[i]
    next_range = ranges[i + 1]
    if next_range[0] <= curr[1] + 1:
        if next_range[1] > curr[1]:
            curr[1] = next_range[1]
        del ranges[i + 1]
    else:
        i += 1

print(f"part 2: {sum(map(lambda x: x[1] - x[0] + 1, ranges))}")
