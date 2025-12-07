from functools import reduce

inp = open("6").read().splitlines()
nums = [list(map(int, i.split())) for i in inp[:-1]]
ops = inp[-1].split()

mult = lambda x, y: x * y
add = lambda x, y: x + y

part1 = 0

for i in range(len(ops)):
    part1 += reduce(
        mult if ops[i] == "*" else add,
        [nums[j][i] for j in range(len(nums))],
        1 if ops[i] == "*" else 0,
    )

for i in range(len(inp)):
    inp[i] += " "


col_index = 0
col_nums = []
part2 = 0

for i in range(len(inp[0])):
    col = "".join([inp[j][i] for j in range(len(nums))])
    if col.strip() != "":
        num = int("".join([inp[j][i] for j in range(len(nums))]))
        col_nums.append(num)
    else:
        part2 += reduce(
            mult if ops[col_index] == "*" else add,
            col_nums,
            1 if ops[col_index] == "*" else 0,
        )
        col_index += 1
        col_nums = []

print(part1)
print(part2)
