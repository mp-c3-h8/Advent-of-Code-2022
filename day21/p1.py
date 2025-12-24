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


def yell(m: str) -> float:
    job = monkeys[m]
    if job.isdigit():
        return int(job)
    ml, op, mr = job.split(' ')
    return OP[op](yell(ml), yell(mr))


ans = yell('root')
print("Part 1:", int(ans))
