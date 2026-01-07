import os.path
from timeit import default_timer as timer
from collections import defaultdict
from typing import Iterator
from heapq import heapify, heappush, heappop

type Pos = complex
type Dir = complex
type Valley = defaultdict[Pos, list[Dir]]  # (pos, list of blizzard directions at pos)
type Item = tuple[Pos, int]  # (pos,minutes_passed)
type Prio = tuple[int, int]
type PrioItem = tuple[Prio, int, Item]  # (prio,counter,Item)


def create_map(data: str) -> tuple[Valley, int, int]:
    DIR: dict[str, Dir] = {"<": -1, ">": 1, "^": -1j, "v": 1j}
    split = data.splitlines()
    dimy, dimx = len(split)-2, len(split[0])-2
    # exclude walls
    res = defaultdict(list, {(x-1) + (y-1)*1j: [DIR[c]]
                             for y, row in enumerate(split)
                             for x, c in enumerate(row) if c not in ".#"})
    return (res, dimy, dimx)


def print_valley(valley: Valley, dimy: int, dimx: int) -> None:
    DIR_INV: dict[Dir, str] = {-1: "<", 1: ">", -1j: "^",  1j: "v"}
    s = [["." for _ in range(dimx)] for _ in range(dimy)]
    for pos, blizz in valley.items():
        if len(blizz) == 1:
            s[int(pos.imag)][int(pos.real)] = DIR_INV[blizz[0]]
        else:
            s[int(pos.imag)][int(pos.real)] = str(len(blizz))
    res = "".join("".join(c for c in row) + "\n" for row in s)
    print(res)


def blizzards_move(valley: Valley, dimy: int, dimx: int, count: int = 1) -> Valley:
    for _ in range(count):
        res = defaultdict(list)
        for pos, blizz in valley.items():
            for b in blizz:
                new_pos = complex((pos.real+b.real) % dimx, (pos.imag+b.imag) % dimy)
                res[new_pos].append(b)
        valley = res
    return valley


def neighbors(pos: Pos) -> Iterator[Pos]:
    yield from (pos+d for d in (1, -1, 1j, -1j))


def in_valley(pos: Pos, dimy: int, dimx: int) -> bool:
    return (0 <= int(pos.real) < dimx) and (0 <= int(pos.imag) < dimy)


def to_goal(pos: Pos, goal: Pos) -> int:
    diff = pos-goal
    return abs(int(diff.real)) + abs(int(diff.imag))


def avoid_blizzards(valley: Valley, dimy: int, dimx: int, start: Pos, goal: Pos) -> tuple[int, Valley]:
    states: dict[int, Valley] = {0: valley}  # (minutes_passed,valley_state)
    visited: set[tuple[Pos, int]] = {(start, 0)}  # reached position at minute
    best = 10**5

    item: Item = (start, 0)  # (pos,minutes_passed)
    prio: Prio = (to_goal(start, goal), 0)  # (distance to goal, minutes waited)
    q: list[PrioItem] = [(prio, 0, item)]  # (prio,counter,item)
    heapify(q)

    i = 0
    while q:
        prio, _, item = heappop(q)
        dist, m_waited = prio
        pos, m = item

        if m+1 in states:
            new_state = states[m+1]
        else:
            new_state = blizzards_move(states[m], dimy, dimx)
            states[m+1] = new_state

        if pos not in new_state:  # can wait
            if (pos, m+1) not in visited:
                if m+1 + dist < best:  # can we get better?
                    visited.add((pos, m+1))
                    i += 1
                    heappush(q, ((dist, m_waited+1), i, (pos, m+1)))

        for n in neighbors(pos):
            if n == goal:
                best = min(best, m+1)
                continue
            if not in_valley(n, dimy, dimx) or n in new_state:  # cant move to position n
                continue
            if (n, m+1) in visited:  # already been there
                continue
            dist = to_goal(n, goal)
            if m+1 + dist > best:  # cant get better
                continue
            visited.add((n, m+1))
            i += 1
            heappush(q, ((dist, m_waited), i, (n, m+1)))

    return (best, states[best])


def expedition(valley: Valley, dimy: int, dimx: int) -> list[int]:
    start = -1j
    goal = (dimx-1) + (dimy)*1j
    durations = []

    for tour in ((start, goal), (goal, start), (start, goal)):
        start, goal = tour
        duration, valley = avoid_blizzards(valley, dimy, dimx, start, goal)
        durations.append(duration)

    return durations


s = timer()

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

valley, dimy, dimx = create_map(data)
durations = expedition(valley, dimy, dimx)
print("Part 1:", durations[0])
print("Part 2:", sum(durations))


e = timer()
print("time:", e - s)


# debug stuff
# after = blizzards_move(valley, dimy, dimx, 200)
# print_valley(after, dimy, dimx)
