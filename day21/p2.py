import os.path
from operator import add, sub, mul, truediv

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()

monkeys: dict[str, str] = {}
for line in data:
    m, job = line.split(': ')
    monkeys[m] = job

OP = {'+': add, '-': sub, '*': mul, '/': truediv}
INV = {'-': add, '+': sub, '/': mul, '*': truediv}


def find_path(root: str, target: str) -> list[str]:
    if root == target:
        return [root]
    job = monkeys[root]
    if job.isdigit():
        return []
    ml, op, mr = job.split(' ')
    res = find_path(ml, target)
    if res:
        return [root] + res
    res = find_path(mr, target)
    if res:
        return [root] + res
    return []


def yell(m: str) -> float:
    job = monkeys[m]
    if job.isdigit():
        return int(job)
    ml, op, mr = job.split(' ')
    return OP[op](yell(ml), yell(mr))


print("Part 1:", yell('root'))

# its a binary tree
# find the path from root to humn
# traverse that path and evaluate + invert (some) operations
path = find_path('root', 'humn')
humn = None
for i, node in enumerate(path[1:]):
    above = path[i]
    job_above = monkeys[above]
    ml, op, mr = job_above.split(' ')
    val = yell(mr) if ml == node else yell(ml)
    if humn is None:
        humn = val
        continue
    if op in '+*' or ml == node:
        humn = INV[op](humn, val)
    else:
        humn = OP[op](val, humn)

print('Part2:', humn)
