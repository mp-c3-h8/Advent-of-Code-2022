import os.path
from math import prod

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
data = open(input_path).read().splitlines()

grid = {i + j*1j: int(c) for j, row in enumerate(data) for i, c in enumerate(row)}
dimy, dimx = len(data), len(data[0])


def is_visible(pos: complex) -> bool:
    if (
        pos.real == 0 or pos.real == dimx-1
        or pos.imag == 0 or pos.imag == dimy-1
    ):
        return True

    height = grid[pos]
    for d in (1, -1, 1j, -1j):
        visible_from_direction = True
        new_pos = pos + d
        while (new_pos in grid):
            if grid[new_pos] >= height:
                visible_from_direction = False
                break
            new_pos += d
        if visible_from_direction:
            return True

    return False


def scenic_score(pos: complex) -> int:
    height = grid[pos]
    viewing_distances = []
    for d in (1, -1, 1j, -1j):
        s = 0
        new_pos = pos + d
        while (new_pos in grid):
            s += 1
            if grid[new_pos] >= height:
                break
            new_pos += d
        viewing_distances.append(s)
    return prod(viewing_distances)


print("Part 1:", sum(is_visible(pos) for pos in grid))
print("Part 2:", max(scenic_score(pos) for pos in grid))
