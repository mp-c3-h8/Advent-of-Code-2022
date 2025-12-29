import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
data = open(input_path).read().splitlines()

x = 1
values = []  # saves "during"
for instr in data:
    if instr.startswith("n"):
        values.append(x)
        continue
    y = int(instr.split(" ", 1)[1])
    values.append(x)
    values.append(x)
    x += y

ans = sum(values[i-1]*i for i in (20, 60, 100, 140, 180, 220))
print("Part 1:", ans)

crt = ""
for j in range(6):
    row = ""
    for i in range(40):
        pixel = j*40 + i
        x = values[pixel]
        if abs(x - i) <= 1:
            row += "#"
        else:
            row += "."
    crt += row + "\n"

print("Part 2:")
print(crt)
