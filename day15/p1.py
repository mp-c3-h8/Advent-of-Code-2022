import os.path
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

with open(input_path) as f:
    data = f.read().splitlines()

regex = re.compile(r"-?\d+")
y_target = 2_000_000
no_beacon = set()
for line in data:
    sx, sy, bx, by = map(int, regex.findall(line))
    dist = abs(sx-bx) + abs(sy-by)  # manhatten
    ydiff = abs(sy-y_target)
    if ydiff <= dist:
        xdiff = dist-ydiff  # remaining manhatten distance in x-direction
        for x in range(sx-xdiff, sx+xdiff+1):  # sensor included
            no_beacon.add(x)
    if by == y_target:
        no_beacon -= {bx}

print("Part 1:", len(no_beacon))
