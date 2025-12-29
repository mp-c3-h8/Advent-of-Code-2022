import os.path
from itertools import pairwise

type Point = tuple[int, int]
dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")


class Cave:
    def __init__(self, grid: dict[Point, str]) -> None:
        self.grid = grid
        self.y_max = max(y for y, x in grid)
        self.x_min = min(x for y, x in grid)
        self.x_max = max(x for y, x in grid)

    def plot(self) -> None:
        import matplotlib.pyplot as plt
        import numpy as np

        X = np.ones((self.y_max+1, self.x_max - self.x_min+1)) * np.nan
        X[0, 500-self.x_min] = 3

        for (y, x), c in self.grid.items():
            p = (y, x-self.x_min)
            if c == "#":
                X[p] = 1
            elif c == "o":
                X[p] = 2

        plt.imshow(X, cmap="tab20b")
        plt.show()

    def drop_sand(self) -> bool:
        y, x = 0, 500
        occupied = 0
        while occupied != 3:  # nowhere to go -> stop movement
            occupied = 0
            for ny, nx in ((y+1, x), (y+1, x-1), (y+1, x+1)):
                if ny > self.y_max or nx < self.x_min or nx > self.x_max:
                    return False  # into the void
                if (ny, nx) not in self.grid:  # free spot found -> continue movement
                    y, x = ny, nx
                    break
                occupied += 1
        self.grid[(y, x)] = "o"
        return True

    def max_drops(self) -> int:
        drops = 0
        while (self.drop_sand()):
            drops += 1
        return drops


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
print("Part 1:", cave.max_drops())
cave.plot()
