import os.path
from string import ascii_letters
from itertools import batched

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()

PRIO = {letter: i for i, letter in enumerate(ascii_letters, 1)}

p2 = 0
for group in batched(data, 3):
    r1, r2, r3 = group
    badge = set(r1).intersection(r2, r3)
    p2 += PRIO[badge.pop()]

print("Part 2:", p2)
