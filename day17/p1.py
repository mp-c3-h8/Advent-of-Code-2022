import os.path
import inspect
from typing import Iterator
from itertools import cycle
from copy import deepcopy

type Pixel = tuple[int, int]  # (x,y)


class Piece:
    # TODO: __slots__

    def __init__(self, name: str, w: int, h: int, shape: str) -> None:
        self.name = name
        self.w = w
        self.h = h
        self.pixel: set[Pixel] = self._create_pixel(shape)
        self.bound_x = max(x for x, y in self.pixel)
        self.bound_y = max(y for x, y in self.pixel)

    def _create_pixel(self, shape: str) -> set[Pixel]:
        pixel: set[Pixel] = set()
        split = shape.splitlines()
        dimy, dimx = len(split), len(split[0])
        assert (dimy == self.h)
        assert (dimx == self.w)
        for y, row in enumerate(split):
            for x, c in enumerate(row):
                if c == "#":
                    pixel.add((x, dimy-y-1))

        return pixel

    def __str__(self) -> str:
        return f"name: {self.name}\npixel: {self.pixel}"


class Tetris:
    def __init__(self, blueprints: list[Piece], jet: str, w: int = 7, spawn_x: int = 2, spawn_y: int = 3) -> None:
        self.blueprints = blueprints
        self.jet = jet
        self.w = w
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.push = self.push_iterator()
        self.spawn = self.spawn_iterator()
        self.occupied: set[Pixel] = set()
        self.pieces: list[tuple[Piece, Pixel]] = []
        self.max_y: int = 0

    def spawn_iterator(self) -> Iterator[Piece]:
        for piece in cycle(self.blueprints):
            yield deepcopy(piece)

    def push_iterator(self) -> Iterator[int]:
        DIR = {"<": -1, ">": 1}
        for d in cycle(self.jet):
            yield DIR[d]

    def play(self, n: int, plot: bool = False) -> int:
        for _ in range(n):
            self.drop(plot)
        if plot:
            self.plot()
        return self.max_y

    def drop(self, plot: bool) -> None:
        piece = next(self.spawn)
        pos = (self.spawn_x+1, self.max_y + self.spawn_y+1)  # bottom left pixel of the piece's bounding box

        x_offset = 0
        for _ in range(self.spawn_y+1):  # no collisions possible
            d = next(self.push)  # +1 or -1
            if self.piece_can_move_in_x(piece, pos[0], x_offset + d):
                x_offset += d
        pos = (pos[0]+x_offset, pos[1]-self.spawn_y)

        # now we need collision checks
        while True:
            # try to move down
            new_pos = (pos[0], pos[1]-1)
            if new_pos[1] == 0 or self.is_colliding(piece, new_pos):
                break
            pos = new_pos

            # try to move lef/right
            d = next(self.push)
            new_pos = (pos[0]+d, pos[1])
            if not self.piece_can_move_in_x(piece, pos[0], d) or self.is_colliding(piece, new_pos):
                continue
            pos = new_pos

        self.occupied.update((p[0]+pos[0], p[1]+pos[1]) for p in piece.pixel)
        self.max_y = max(self.max_y, pos[1] + piece.bound_y)
        if plot:  # only save if necessary
            self.pieces.append((piece, pos))

    def piece_can_move_in_x(self, piece: Piece, pos_x: int, d: int) -> bool:
        new_x = pos_x + d
        return new_x > 0 and new_x + piece.bound_x <= self.w

    def is_colliding(self, piece: Piece, pos: Pixel) -> bool:
        return any((p[0]+pos[0], p[1]+pos[1]) in self.occupied for p in piece.pixel)

    def plot(self) -> None:
        import numpy as np
        import matplotlib.pyplot as plt

        X = np.ones((self.max_y+1, self.w+1)) * np.nan

        for piece, pos in self.pieces:
            for p in piece.pixel:
                X[p[1]+pos[1], p[0]+pos[0]] = ord(piece.name[0])
        plt.imshow(X, origin="lower", cmap="tab20b")
        plt.xlim((0, self.w))
        plt.show()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

hor = inspect.cleandoc("""
    ....
    ....
    ....
    ####""")
cross = inspect.cleandoc("""
    ....
    .#..
    ###.
    .#..""")
el = inspect.cleandoc("""
    ....
    ..#.
    ..#.
    ###.""")
vert = inspect.cleandoc("""
    #...
    #...
    #...
    #...""")
square = inspect.cleandoc("""
    ....
    ....
    ##..
    ##..""")

h, c, l = Piece("hor", 4, 4, hor), Piece("cross", 4, 4, cross), Piece("l", 4, 4, el)
v, s = Piece("vert", 4, 4, vert), Piece("square", 4, 4, square)
game = Tetris([h, c, l, v, s], data)
ans = game.play(2022,False)
print("Part 1:", ans)

