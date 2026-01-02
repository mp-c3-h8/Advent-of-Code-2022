import os.path
import re
from itertools import combinations
from heapq import heappop, heappush, heapify
from copy import deepcopy

type Node = str
type Edge = tuple[Node, Node]
type Graph = dict[Node, set[Node]]  # node -> {adjacent nodes}
type Weights = dict[Edge, int]  # travel time between nodes. init with 1 for all
type FlowRates = dict[Node, int]
type Item = tuple[int, list[Node]]  # item for prio Q: (minutes_left,opened_valves)
type PrioItem = tuple[int, int, int, Item]  # (prio,counter,sum_press,Item)


def plot_graph(graph: Graph, weights: Weights) -> None:
    import networkx as nx
    import matplotlib.pyplot as plt
    G = nx.Graph()
    G.add_nodes_from(graph)
    G.add_weighted_edges_from(edge + (flow,) for edge, flow in weights.items())

    pos = nx.spring_layout(G, seed=1)
    nx.draw_networkx_nodes(G, pos, node_size=700)
    nx.draw_networkx_edges(G, pos, width=4)
    nx.draw_networkx_labels(G, pos, font_size=15, font_family="sans-serif")
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=15)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def create_graph(data: str) -> tuple[Graph, Weights, FlowRates]:
    graph: Graph = {}
    weights: Weights = {}
    flow_rates: FlowRates = {}
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
        flow_rates[node] = int(flow_str)

    return (graph, weights, flow_rates)


def remove_node(graph: Graph, weights: Weights, flow_rates: FlowRates, node: Node) -> None:
    adj = list(graph[node])
    for n1, n2 in combinations(adj, 2):
        if (n1, n2) not in weights:
            weights[(n1, n2)] = weights[(n1, node)] + weights[(n2, node)]
            weights[(n2, n1)] = weights[(n1, node)] + weights[(n2, node)]
            graph[n1].add(n2)
            graph[n2].add(n1)
    for a in adj:
        graph[a].remove(node)
        del weights[(node, a)]
        del weights[(a, node)]
    del weights[(node, node)]
    del flow_rates[node]
    del graph[node]


def simpflify_graph(graph: Graph, weights: Weights, flow_rates: FlowRates, start: Node) -> None:
    # delete zero flow rate nodes and adjust weights
    nodes = list(graph)
    for node in nodes:
        if node != start and flow_rates[node] == 0:
            remove_node(graph, weights, flow_rates, node)


def floyd_warshall(graph: Graph, weights: Weights) -> Weights:
    # https://www.geeksforgeeks.org/dsa/floyd-warshall-algorithm-dp-16/
    nodes = list(graph)
    shortest_paths = deepcopy(weights)

    for k in nodes:
        for i in nodes:
            for j in nodes:
                w_ij = shortest_paths[(i, j)] if (i, j) in shortest_paths else 10**10
                w_ik = shortest_paths[(i, k)] if (i, k) in shortest_paths else 10**10
                w_kj = shortest_paths[(k, j)] if (k, j) in shortest_paths else 10**10
                shortest_paths[(i, j)] = min(w_ij, w_ik + w_kj)
    return shortest_paths


def estimate_pressure(node: Node, flow: FlowRates, shortest_paths: Weights, m: int, closed: set[Node]) -> int:
    # best case for the remaining amount of pressure: (upper bound)
    time_to_next = min(shortest_paths[(node, e)] for e in closed)
    if m-time_to_next < 2:
        return 0
    travel_times = sorted([shortest_paths[(e1, e2)] for e1, e2 in combinations(closed, 2)])
    flow_rates = sorted([flow[n] for n in closed], reverse=True)
    estimate = (m-time_to_next-1) * flow_rates[0]
    m -= time_to_next+1
    for t, f in zip(travel_times, flow_rates[1:]):
        if m - t < 2:
            break
        estimate += (m-t-1) * f
        m -= t+1
    return estimate


def max_pressure(graph: Graph, shortest_paths: Weights, flow: FlowRates, start: Item, elephant: bool = False) -> int:
    # prio: highest total pressure comes first -> "best" grows faster
    q: list[PrioItem] = [(0, 0, 0, start)]  # ( prio, counter, sum_press, (minutes_left,opened_valves) )
    heapify(q)
    best = 0
    avail = set(graph)

    i = 0
    while q:
        _prio, _count, p, item = heappop(q)
        m, opened = item
        last_opened = opened[-1]
        closed = avail.difference(set(opened))

        if elephant:
            # elephant always starts at "start"
            p_ele = max_pressure(graph, shortest_paths, flow, (26, opened + start[1]))
        else:
            p_ele = 0
        if p + p_ele + estimate_pressure(last_opened, flow, shortest_paths, m, closed) < best:
            continue
        best = max(best, p + p_ele)


        for node in closed:  # go to node and open valve
            w = shortest_paths[(last_opened, node)]
            if m-w < 2:
                continue
            new_p = p + (m-w-1)*flow[node]
            new_opened = opened + [node]
            new_closed = closed.difference({node})
            if len(new_closed) == 0:
                continue
            i += 1
            heappush(q, (-new_p, i, new_p, (m-w-1, new_opened)))
    return best


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

graph, weights, flow = create_graph(data)
simpflify_graph(graph, weights, flow, "AA")
shortest_paths = floyd_warshall(graph, weights)
p1 = max_pressure(graph, shortest_paths, flow, (30, ["AA"]))
print("Part 1:", p1)
p2 = max_pressure(graph, shortest_paths, flow, (26, ["AA"]), True)
print("Part 2:", p2)

# plot_graph(graph, weights)
