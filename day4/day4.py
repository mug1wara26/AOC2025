inp = [list(i) for i in open("4").read().splitlines()]


def in_bounds(row, col) -> bool:
    return row >= 0 and row < len(inp) and col >= 0 and col < len(inp[0])


def num_rolls_surrounding(row, col):
    ret = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if (dr, dc) != (0, 0) and in_bounds(dr + row, dc + col):
                ret += 1 if inp[row + dr][col + dc] == "@" else 0

    return ret


total = 0
additional = 1
while additional != 0:
    additional = 0
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            if inp[i][j] == "@" and num_rolls_surrounding(i, j) < 4:
                additional += 1
                inp[i][j] = "."

    total += additional
    print(total)


print(total)
