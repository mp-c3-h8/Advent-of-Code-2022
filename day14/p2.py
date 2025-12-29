import os.path
from itertools import pairwise

type Point = tuple[int, int]
dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")


class Cave:
    def __init__(self, grid: dict[Point, str]) -> None:
        self.grid = grid
        self.y_max = max(y for y, x in grid) + 2
        self.hole = (0, 500)

    def plot(self) -> None:
        import matplotlib.pyplot as plt
        import numpy as np

        x_min = min(x for y, x in self.grid)
        x_max = max(x for y, x in self.grid)
        X = np.ones((self.y_max+1, x_max - x_min+1)) * np.nan
        X[0, 500-x_min] = 3
        X[self.y_max, :] = 1

        for (y, x), c in self.grid.items():
            p = (y, x-x_min)
            if c == "#":
                X[p] = 1
            elif c == "o":
                X[p] = 2

        plt.imshow(X, cmap="tab20b")
        plt.show()

    def drop_sand(self) -> bool:
        y, x = self.hole

        while True:
            ny = y+1
            if ny == self.y_max:  # floor
                break
            if (ny, x) not in self.grid:
                y, x = ny, x
            elif (ny, x-1) not in self.grid:
                y, x = ny, x-1
            elif (ny, x+1) not in self.grid:
                y, x = ny, x+1
            else:  # nowhere to go
                break

        self.grid[(y, x)] = "o"
        return False if (y, x) == self.hole else True

    def max_drops(self) -> int:
        drops = 0
        while (self.drop_sand()):
            drops += 1
        return drops+1


def create_cave(data: str) -> Cave:
    grid: dict[Point, str] = {}

    for line in data.splitlines():
        paths = line.split(" -> ")
        for p1, p2 in pairwise(paths):
            x1, y1 = map(int, p1.split(","))
            x2, y2 = map(int, p2.split(","))
            for y in range(min(y1, y2), max(y1, y2)+1):
                for x in range(min(x1, x2), max(x1, x2)+1):
                    grid[(y, x)] = "#"

    return Cave(grid)


cave = create_cave(open(input_path).read())
print("Part 2:", cave.max_drops())
cave.plot()
