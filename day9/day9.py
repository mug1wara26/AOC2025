import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

start_time = time.time()
inp = list(map(lambda x: tuple(map(int, x.split(","))), open("9").read().splitlines()))


def area(p1, p2):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


max_area = 0

for i in range(len(inp)):
    for j in range(i + 1, len(inp)):
        max_area = max(max_area, area(inp[i], inp[j]))

print(f"Part 1: {max_area}")

vertical_lines = sorted(
    [sorted(inp[i : i + 2], key=lambda x: x[1]) for i in range(0, len(inp), 2)],
    key=lambda x: x[0][0],
)

horizontal_lines = [
    sorted(inp[i : i + 2], key=lambda x: x[0]) for i in range(1, len(inp) - 1, 2)
]


def in_poly(p):
    # Ray cast to left
    num_crossings = 0
    lows = set()
    highs = set()
    for line in vertical_lines:
        if line[0][0] >= p[0]:
            break
        if line[0][1] <= p[1] <= line[1][1]:
            if line[0][1] == p[1] and p[1] in highs:
                continue
            if line[1][1] == p[1] and p[1] in lows:
                continue
            lows.add(line[0][1])
            highs.add(line[1][1])
            num_crossings += 1

    return num_crossings % 2 == 1


longest_two = sorted(
    horizontal_lines, key=lambda x: abs(x[0][0] - x[1][0]), reverse=True
)
mid1 = (
    longest_two[0][0]
    if longest_two[0][0][0] > longest_two[0][1][0]
    else longest_two[0][1]
)
mid2 = (
    longest_two[1][0]
    if longest_two[1][0][0] > longest_two[1][1][0]
    else longest_two[1][1]
)

if mid1[1] < mid2[1]:
    mid1, mid2 = mid2, mid1

mid1_ylimit = 0
mid2_ylimit = 0
for i in horizontal_lines:
    if i[0][1] > mid1[1] and i[0][0] <= mid1[0] <= i[1][0]:
        mid1_ylimit = i[0][1]
    if i[0][1] < mid2[1] and i[0][0] <= mid2[0] <= i[1][0]:
        mid2_ylimit = i[0][1]


point = []
max_area = 0

for p in inp:
    m = None
    if p[0] >= mid1[0]:
        continue
    if mid1[1] <= p[1] <= mid1_ylimit:
        m = mid1
    elif mid2[1] <= p[1] <= mid2_ylimit:
        m = mid2
    if m is not None:
        p1, p2 = (p[0], m[1]), (m[0], p[1])
        if (a := area(m, p)) > max_area and in_poly(p1) and in_poly(p2):
            max_area = a
            point = [p if p[1] < m[1] else p1, abs(p[0] - m[0]), abs(p[1] - m[1])]
print(f"Part 2: {max_area}")
print(f"Execution time: {time.time() - start_time}")
rect = patches.Rectangle(
    point[0],
    point[1],
    point[2],
    facecolor="lightblue",
    edgecolor="blue",
    linewidth=2,
)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.add_patch(rect)
x = [i[0] for i in inp]
y = [i[1] for i in inp]
for i in range(len(inp) - 1):
    plt.plot(x[i : i + 2], y[i : i + 2], "ro-")
plt.show()
