import heapq
from itertools import combinations
from ufds import DisjointSet
import math
import time


def distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


start = time.time()
data = list(
    map(
        lambda x: (distance(x[0], x[1]), x[0], x[1]),
        combinations(
            tuple(
                map(
                    lambda x: tuple(map(int, x.split(","))),
                    open("8").read().splitlines(),
                )
            ),
            2,
        ),
    )
)

heapq.heapify(data)

ds = DisjointSet()
i = 0
n = 1000

while True:
    pair = heapq.heappop(data)
    i += 1
    if ds.find(pair[1]) != ds.find(pair[2]):
        n -= 1
        ds.union(pair[1], pair[2])
    if i == 1000:
        print(f"Part 1: {math.prod(sorted(map(len, list(ds)), reverse=True)[:3])}")

    if n == 1:
        print(f"Part 2: {pair[1][0] * pair[2][0]}")
        break
print(time.time() - start)
