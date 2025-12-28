import os.path
from more_itertools import sliding_window

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

signal = open(input_path).read()

p = []
for k in [4, 14]:
    for i, window in enumerate(sliding_window(signal, k)):
        if len(set(window)) == k:
            p.append(i+k)
            break

print("Part 1:", p[0])
print("Part 2:", p[1])
