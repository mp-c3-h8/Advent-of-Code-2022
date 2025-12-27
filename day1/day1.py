import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().split("\n\n")

calories = sorted([sum(map(int, elve.splitlines())) for elve in data])

print("Part 1:", calories[-1])
print("Part 2:", sum(calories[-3:]))
