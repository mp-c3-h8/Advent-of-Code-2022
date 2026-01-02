import os.path
import re
from itertools import combinations, product
from collections import defaultdict, deque

type Node = str
type Edge = tuple[Node, Node]
type Graph = dict[Node, set[Node]]  # node -> {adjacent nodes}
type Weights = defaultdict[Edge, int]   # travel time between nodes. init with 1 for all
type FlowRates = dict[Node, int]
type Item = tuple[Node, int, int, set[Node], int]  # item for Q: (curr,minutes_left,sum_press,closed_valves,bitmask)


def create_graph(data: str) -> tuple[Graph, Weights, FlowRates]:
    graph: Graph = {}
    weights: Weights = defaultdict(lambda: 10**10)
    flow: FlowRates = {}
    regex = re.compile(r"([A-Z]{2})(?:[a-z= ]+)(\d*)(?:[a-z; ]+)(.*)")

    for line in data.splitlines():
        found = regex.findall(line)
        node, flow_str, adj_str = found[0]
        adj = adj_str.split(", ")
        graph[node] = set(adj)
        weights[(node, node)] = 0
        for a in adj:
            weights[(node, a)] = 1
            weights[(a, node)] = 1
        if flow_str != "0":  # ignore 0 pressure nodes
            flow[node] = int(flow_str)

    return (graph, weights, flow)


def floyd_warshall(graph: Graph, weights: Weights) -> None:
    # https://www.geeksforgeeks.org/dsa/floyd-warshall-algorithm-dp-16/
    # in place
    for k, i, j in product(graph, repeat=3):
        weights[(i, j)] = min(weights[(i, j)], weights[(i, k)] + weights[(k, j)])


def calc_all_pressures(flow: FlowRates, weights: Weights, limit: int, start: Node) -> dict[int, int]:
    # calculate max pressure for every configuration of opened valves
    indices: dict[str, int] = {node: 1 << i for i, node in enumerate(flow)}  # 1,2,4,8 etc
    all_pressures: defaultdict[int, int] = defaultdict(int)
    avail = set(flow)  # no 0 flow nodes in here

    init: Item = (start, limit, 0, avail, 0)
    q: deque[Item] = deque([init])
    while q:
        curr, m, p, avail, mask = q.pop()

        all_pressures[mask] = max(all_pressures[mask], p)

        for node in avail:
            w = weights[(curr, node)]
            if m-w < 2:
                continue
            new_m = (m-w-1)
            new_p = p + new_m * flow[node]
            new_avail = avail - {node}
            new_mask = mask + indices[node]
            q.append((node, new_m, new_p, new_avail, new_mask))

    return all_pressures


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

graph, weights, flow = create_graph(data)
# no need to simplify graph:
# floyd warshall + non zero flow dict is sufficient
floyd_warshall(graph, weights)
all_flows = calc_all_pressures(flow, weights, 30, "AA")
print("Part 1:", max(f for f in all_flows.values()))

all_flows = calc_all_pressures(flow, weights, 26, "AA")
# combine 2 disjoint paths
p2 = max(f1+f2 for (mask1, f1), (mask2, f2) in combinations(all_flows.items(), 2) if not mask1 & mask2)
print("Part 2:", p2)
