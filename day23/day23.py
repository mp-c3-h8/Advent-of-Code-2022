import os.path
from timeit import default_timer as timer
from enum import Enum
from collections import defaultdict, deque

type Pos = complex


class DIRS(Enum):
    NW = -1-1j
    N = -1j
    NE = 1-1j
    E = 1
    SE = 1+1j
    S = 1j
    SW = -1+1j
    W = -1


def elves_bound(elves: set[Pos]) -> tuple[int, int, int, int]:
    x_max = max(int(elf.real) for elf in elves)
    x_min = min(int(elf.real) for elf in elves)
    y_max = max(int(elf.imag) for elf in elves)
    y_min = min(int(elf.imag) for elf in elves)
    return (x_min, x_max, y_min, y_max)


def plot_elves(elves: set[Pos]) -> None:
    import numpy as np
    import matplotlib.pyplot as plt

    (x_min, x_max, y_min, y_max) = elves_bound(elves)
    dimy, dimx = y_max-y_min+1, x_max-x_min+1

    X = np.ones((dimy, dimx)) * np.nan

    for elf in elves:
        X[int(elf.imag)-y_min, int(elf.real)-x_min] = 1
    plt.imshow(X, cmap="tab20b")
    plt.show()


def spreadout(elves: set[Pos], rounds: int | None = None) -> tuple[set[Pos], int]:

    if rounds is None:
        rounds = 3*10**3

    dirs = deque([
        (DIRS.N, (DIRS.NW, DIRS.N, DIRS.NE)),
        (DIRS.S, (DIRS.SE, DIRS.S, DIRS.SW)),
        (DIRS.W, (DIRS.SW, DIRS.W, DIRS.NW)),
        (DIRS.E, (DIRS.NE, DIRS.E, DIRS.SE)),
    ])

    i = 0
    proposals: defaultdict[Pos, list[Pos]] = defaultdict(list)
    for i in range(rounds):
        proposals.clear()
        new_elves: set[Pos] = elves.copy()
        for elf in elves:
            if all(elf + d.value not in elves for d in DIRS):
                continue
            for d, to_check in dirs:
                if all(elf + c.value not in elves for c in to_check):
                    proposals[elf + d.value].append(elf)
                    new_elves.remove(elf)
                    break

        if len(proposals) == 0:
            break

        for new_pos, moves in proposals.items():
            if len(moves) == 1:
                new_elves.add(new_pos)
            else:
                new_elves.update(moves)

        elves = new_elves
        dirs.rotate(-1)
    return (elves, i+1)


def part1(elves: set[Pos]) -> int:
    (x_min, x_max, y_min, y_max) = elves_bound(elves)
    dimy, dimx = y_max-y_min+1, x_max-x_min+1
    return dimy*dimx-len(elves)


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read().splitlines()

elves = {i + j*1j for j, row in enumerate(data) for i, c in enumerate(row) if c == "#"}

after, rounds = spreadout(elves, 10)
print("Part 1:",  part1(after))

after, rounds = spreadout(elves)
print("Part 2:",  rounds)
# plot_elves(after)

e = timer()
print("time:", e - s)
