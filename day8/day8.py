import heapq
from itertools import combinations
from ufds import DisjointSet
import math


class Pair:
    def __init__(self, a, b) -> None:
        self.a = a
        self.b = b
        self.distance = (
            (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
        ) ** 0.5

    def __repr__(self) -> str:
        return f"({self.a}, {self.b})"

    def __lt__(self, other):
        return self.distance < other.distance


data = list(
    map(
        lambda x: Pair(x[0], x[1]),
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

while True:
    pair = heapq.heappop(data)
    i += 1
    ds.union(pair.a, pair.b)
    if i == 1000:
        print(f"Part 1: {math.prod(sorted(map(len, list(ds)), reverse=True)[:3])}")

    if len(list(ds)[0]) == 1000:
        print(f"Part 2: {pair.a[0] * pair.b[0]}")
        break
