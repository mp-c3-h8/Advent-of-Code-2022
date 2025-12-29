import os.path
from collections import deque
from math import inf

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")


def build_graph(data: str) -> tuple[dict[complex, int], complex, complex]:
    data_split = data.splitlines()
    grid: dict[complex, int] = {}
    start, end = 0, 0
    for j, row in enumerate(data_split):
        for i, c in enumerate(row):
            pos = i+j*1j
            if c == "S":
                start = pos
                val = ord("a")
            elif c == "E":
                end = pos
                val = ord("z")
            else:
                val = ord(c)
            grid[pos] = val
    return (grid, start, end)


def bfs(graph: dict[complex, int], starts: list[complex], end: complex) -> int | float:
    '''
    bfs checks ALL path with length 0, then ALL with length 1 etc
    similar to how dijkstra with prio queue works
    '''
    init = [(start, 0) for start in starts]
    q: deque[tuple[complex, int]] = deque(init)
    seen: set[complex] = set(starts)

    while q:
        pos, steps = q.popleft()

        # first hit is shortest path cuz of bfs
        if pos == end:
            return steps

        # seen check moved down and initialized with starts

        for d in (1, -1, 1j, -1j):
            new_pos = pos + d
            if new_pos in graph and graph[new_pos] <= graph[pos] + 1:
                # when seen, we already came here with less steps cuz of bfs
                # seen check here to keep queue short
                if new_pos not in seen:
                    seen.add(new_pos)
                    q.append((new_pos, steps+1))
    return inf


data = open(input_path).read()
graph, start, end = build_graph(data)
print("Part 1:", bfs(graph, [start], end))

starts = [pos for pos, height in graph.items() if height == ord("a")]
print("Part 2:", bfs(graph, starts, end))
