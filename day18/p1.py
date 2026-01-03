import os.path


def surface(data: str) -> int:
    res = 0
    droplet = set()
    for line in data.splitlines():
        cube = tuple(map(int, line.split(",")))  # (x1,x2,x3)
        touching = sum(
            (cube[:i] + (x+d,) + cube[i+1:] in droplet)
            for i, x in enumerate(cube)
            for d in (1, -1)
        )
        droplet.add(cube)
        res += 6 - 2*touching
    return res


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

ans = surface(data)
print("Part 1:", ans)
