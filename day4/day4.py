import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()


def intersection(x: range, y: range) -> range:
    return range(max(x.start, y.start), min(x.stop, y.stop))


p1, p2 = 0, 0
for line in data:
    i1, i2 = line.split(",", 1)
    a, b = map(int, i1.split("-", 1))  # interval [a,b]
    c, d = map(int, i2.split("-", 1))  # interval [c,d]
    x, y = range(a, b+1), range(c, d+1)
    inter = intersection(x, y)
    if inter == x or inter == y:
        p1 += 1
        p2 += 1
    elif inter:  # true if not empty
        p2 += 1

print("Part 1:", p1)
print("Part 2:", p2)
