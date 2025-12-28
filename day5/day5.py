import os.path
from collections import defaultdict
import re
from copy import deepcopy

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

stacks_str, moves_str = open(input_path).read().split("\n\n")

stacks: dict[int, list[str]] = defaultdict(list)

for line in stacks_str.splitlines():
    for i, c in enumerate(line, 1):
        if c.isalpha():
            stacks[i//4+1].insert(0, c)

stacks = {i: stacks[i] for i in sorted(stacks)}
stacks2 = deepcopy(stacks)

for move in moves_str.splitlines():
    amount, source, target = map(int, re.findall(r"\d+", move))
    rest, to_move = stacks[source][:-amount], stacks[source][-amount:]
    rest2, to_move2 = stacks2[source][:-amount], stacks2[source][-amount:]

    stacks[source] = rest
    stacks[target] += reversed(to_move)

    stacks2[source] = rest2
    stacks2[target] += to_move2

print("Part 1:", "".join(stack[-1] for stack in stacks.values()))
print("Part 2:", "".join(stack[-1] for stack in stacks2.values()))