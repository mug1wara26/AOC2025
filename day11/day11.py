from functools import cache
import time

start = time.time()

edges = {
    i[: i.index(":")]: i[i.index(" ") :].strip().split()
    for i in open("11").read().splitlines()
}

edges["out"] = []


@cache
def num_paths(src, dst):
    ret = 0
    for i in edges[src]:
        if i == dst:
            ret += 1
        else:
            ret += num_paths(i, dst)

    return ret


print(f"part 1: {num_paths('you', 'out')}")
part2 = num_paths("svr", "fft") * num_paths("fft", "dac") * num_paths("dac", "out")
print(f"part 2: {part2}")

print(time.time() - start)
