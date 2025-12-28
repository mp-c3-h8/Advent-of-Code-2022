import os.path
from string import ascii_letters

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()

PRIO = {letter: i for i, letter in enumerate(ascii_letters, 1)}

p1 = 0
for rucksack in data:
    l = len(rucksack)//2
    left, right = rucksack[:l], rucksack[l:]
    in_both = set(left).intersection(right)
    p1 += PRIO[in_both.pop()]

print("Part 1:", p1)
