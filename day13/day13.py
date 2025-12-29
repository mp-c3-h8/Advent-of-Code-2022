import os.path
from functools import cmp_to_key
from math import prod

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read()


def in_order(left: list | int, right: list | int) -> int:
    match left, right:
        case int(), int():
            if left < right:
                return -1
            if left > right:
                return 1
            return 0
        case int(), list():
            left = [left]
        case list(), int():
            right = [right]

    # both lists
    for l, r in zip(left, right):
        if (res := in_order(l, r)) != 0:
            return res

    return in_order(len(left), len(right))


ans = 0
for i, line in enumerate(data.split("\n\n"), 1):
    left, right = line.splitlines()
    res = in_order(eval(left), eval(right))
    if res == -1:
        ans += i
print("Part 1:", ans)

divider = [[[2]], [[6]]]
all_packets = [eval(p) for p in data.replace("\n\n", "\n").splitlines()] + divider
all_packets = sorted(all_packets, key=cmp_to_key(in_order))
print("Part 2:", prod(all_packets.index(d)+1 for d in divider))
