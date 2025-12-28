import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
data = open(input_path).read().splitlines()

DIRS: dict[str, complex] = {"R": 1, "L": -1, "U": 1j, "D": -1j}


def count_visited(data: list[str], num_tails: int = 1) -> int:
    head = 0
    tails = [0]*num_tails
    seen = set()
    for motion in data:
        d_str, steps_str = motion.split(" ", 1)
        d = DIRS[d_str]
        for i in range(int(steps_str)):
            head += d
            curr = head
            for k in range(num_tails):
                tail = tails[k]
                diff = curr-tail
                if abs(diff) > 1.5:  # diag would be sqrt(2)
                    if int(diff.real):
                        tail += diff.real/abs(diff.real)
                    if int(diff.imag):
                        tail += diff.imag/abs(diff.imag) * 1j
                tails[k] = tail
                curr = tail
            seen.add(curr)
    return len(seen)


print("Part 1:", count_visited(data))
print("Part 2:", count_visited(data, 9))
