import os.path
import re
from timeit import default_timer as timer


type Pos = complex
type Dir = complex
type Board = dict[Pos, str]


def create_board(data: str) -> tuple[Board, Pos, int, int]:
    rows = data.splitlines()
    board = {
        i + j*1j: c
        for j, row in enumerate(rows)
        for i, c in enumerate(row) if c != " "
    }
    dimy, dimx = len(rows), max(len(row) for row in rows)
    startx = rows[0].index(".")
    return (board, complex(startx, 0), dimy, dimx)


def create_teleport_map(board: Board, dimy: int, dimx: int) -> dict[tuple[Pos, Dir], Pos]:
    DIRS = (1, -1, 1j, -1j)
    teleport_map:  dict[tuple[Pos, Dir], Pos] = {}

    for pos in board:
        for d in DIRS:
            new_pos = move_with_wrap(pos, d, dimy, dimx)
            if new_pos in board or (new_pos, d) in teleport_map:
                continue

            # need to teleport
            tele = new_pos
            while (tele not in board):
                tele = move_with_wrap(tele, d, dimy, dimx)
            teleport_map[(new_pos, d)] = tele

            # symmetry
            tele_back = move_with_wrap(tele, -d, dimy, dimx)
            if tele_back not in board:
                teleport_map[(tele_back, -d)] = pos
    return teleport_map


def move_with_wrap(pos: Pos, d: Dir, dimy: int, dimx: int) -> Pos:
    new_pos = pos+d
    return complex(new_pos.real % dimx, new_pos.imag % dimy)


def move(board: Board, tele: dict[tuple[Pos, Dir], Pos], pos: Pos, d: Dir, steps: int, dimy: int, dimx: int) -> Pos:
    for _ in range(steps):
        new_pos = move_with_wrap(pos, d, dimy, dimx)
        if new_pos not in board:
            new_pos = tele[(new_pos, d)]
        if board[new_pos] == "#":
            break
        pos = new_pos
    return pos


def password(pos: Pos, d: Dir) -> int:
    FACING = {1: 0, 1j: 1, -1: 2, -1j: 3}
    row = int(pos.imag) + 1
    col = int(pos.real) + 1
    pwd = 1000*row + 4*col + FACING[d]
    return pwd


def follow(board: Board, path: str, start_pos: Pos, start_dir: Dir, dimy: int, dimx: int) -> int:
    tele = create_teleport_map(board, dimy, dimx)
    pos, d = start_pos, start_dir
    TURN = {"R": 1j, "L": -1j}  # y-axis downwards
    for inst in re.findall(r"(\d+|[RL])", path):
        if inst in "RL":
            d *= TURN[inst]
        else:
            steps = int(inst)
            pos = move(board, tele, pos, d, steps, dimy, dimx)
    return password(pos, d)


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

board_raw, path = data.split("\n\n")
board, start, dimy, dimx = create_board(board_raw)
pwd = follow(board, path, start, 1, dimy, dimx)

print("Part 1:", pwd)

e = timer()
print("time:", e - s)
