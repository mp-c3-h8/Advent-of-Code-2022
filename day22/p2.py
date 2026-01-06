import os.path
import re

type Pos = complex
type Dir = complex
type PosDir = tuple[Pos, Dir]
type Board = dict[Pos, str]
type Face = dict[Dir, tuple[str, Dir, Pos] | None]


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


def switch_face(pos: Pos, d: Dir, exp: Pos = 0) -> PosDir:
    # pos is a global coordinate
    # we are on an edge
    # {walking dir: (new_face,rotation,correction)}->  y downwards!
    AA: Face = {-1j: ("EE", 1j, 0), 1: None, 1j: None, -1: ("DD", -1, -1j)}
    BB: Face = {-1j: ("EE", 1, -1j), 1: ("CC", -1, -2-1j), 1j: ("FF", 1j, -2), -1: None}
    CC: Face = {-1j: None, 1: ("BB", -1, -2-1j), 1j: ("EE", 1j, -2), -1: None}
    DD: Face = {-1j: ("FF", 1j, 0), 1: None, 1j: None, -1: ("AA", -1, -1j)}
    EE: Face = {-1j: None, 1: ("CC", -1j, -2j), 1j: ("BB", 1, 1j), -1: ("AA", -1j, 0)}
    FF: Face = {-1j: None, 1: ("BB", -1j, -2j), 1j: None, -1: ("DD", -1j, 0)}

    FACES: dict[str, Face] = {"AA": AA, "BB": BB, "CC": CC, "DD": DD, "EE": EE, "FF": FF}

    # position in "face grid" (y,x)
    FACEGRID = {(0, 1): "AA", (0, 2): "BB", (1, 1): "FF", (2, 0): "DD", (2, 1): "CC", (3, 0): "EE"}
    FACEGRID_INV = {val: key for key, val in FACEGRID.items()}
    FACE_WIDTH = 50

    # calc local coordinates
    local_pos = complex(pos.real % FACE_WIDTH, pos.imag % FACE_WIDTH)
    facegrid_pos = (int(pos.imag // FACE_WIDTH), int(pos.real // FACE_WIDTH))
    face_str = FACEGRID[facegrid_pos]
    face = FACES[face_str]

    val = face[d]
    assert (val is not None)
    new_face_str, rot, corr = val
    new_facegrid_pos = FACEGRID_INV[new_face_str]

    new_local_pos = local_pos*rot
    new_local_pos += corr  # manually created with tests
    new_local_pos = complex(new_local_pos.real % FACE_WIDTH, new_local_pos.imag % FACE_WIDTH)

    new_d = d*rot
    # back to global coordinates
    new_pos = complex(new_local_pos.real + new_facegrid_pos[1] * FACE_WIDTH,
                      new_local_pos.imag + new_facegrid_pos[0] * FACE_WIDTH)
    
    if exp:
        print(f"{face_str} -> {new_face_str}: - Expected: {exp} Calculated: {local_pos} -> {new_local_pos} Error: {new_local_pos-exp} (global: {new_pos})")

    return (new_pos, new_d)


def move(board: Board, pos: Pos, d: Dir, steps: int, dimy: int, dimx: int) -> PosDir:
    for _ in range(steps):
        new_pos = pos+d
        new_d = d
        if new_pos not in board:
            new_pos, new_d = switch_face(pos, d)
        if board[new_pos] == "#":
            break
        pos = new_pos
        d = new_d

    return (pos, d)


def password(pos: Pos, d: Dir) -> int:
    FACING = {1: 0, 1j: 1, -1: 2, -1j: 3}
    row = int(pos.imag) + 1
    col = int(pos.real) + 1
    pwd = 1000*row + 4*col + FACING[d]
    return pwd


def follow(board: Board, path: str, start_pos: Pos, start_dir: Dir, dimy: int, dimx: int) -> int:
    pos, d = start_pos, start_dir
    TURN = {"R": 1j, "L": -1j}  # y-axis downwards
    for inst in re.findall(r"(\d+|[RL])", path):
        if inst in "RL":
            d *= TURN[inst]
        else:
            steps = int(inst)
            pos, d = move(board, pos, d, steps, dimy, dimx)
    return password(pos, d)


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

board_raw, path = data.split("\n\n")
board, start, dimy, dimx = create_board(board_raw)
pwd = follow(board, path, start, 1, dimy, dimx)
print("Part 2:", pwd)


tests = [
    ["A nach oben zu E", 90+0*1j, -1j, 0+40j],
    ["A nach links zu D", 50+40*1j, -1, 0+9j],  # inv
    ["B nach oben zu E", 140+0*1j, -1j, 40+49j],
    ["B nach rechts zu C", 149+40*1j, 1, 49+9j],  # inv
    ["B nach unten zu F", 140+49*1j, 1j, 49+40j],
    ["F nach links zu D", 50+90j, -1, 40],
    ["F nach rechts zu B", 99+90j, 1, 40+49j],
    ["C nach rechts zu B", 99+140j, 1, 49+9j],  # inv
    ["C nach unten zu E", 90+149j, 1j, 49+40j],
    ["D nach oben zu F", 40+100j, -1j, 0+40j],
    ["D nach links zu A", 0+140j, -1, 0+9j],  # inv
    ["E nach links zu A", 0+190j, -1, 40],
    ["E nach rechts zu C", 49+190j, 1, 40+49j],
    ["E nach unten zu B", 40+199j, 1j, 40],
]

# for desc, pos, d, exp in tests:
#     switch_face(pos, d, exp)
