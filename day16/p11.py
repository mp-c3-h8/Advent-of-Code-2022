import os.path
import re
from itertools import combinations
from heapq import heappop, heappush, heapify

type Node = str
type Edge = tuple[Node, Node]
type Graph = dict[Node, set[Node]]  # node -> {adjacent nodes}
type Weights = dict[Edge, int]  # travel time between nodes. init with 1 for all
type FlowRates = dict[Node, int]
type Item = tuple[Node, int, int, set[Node]]  # item for prio Q: (candidate,minutes_left,sum_press,opened_valves)
type PrioItem = tuple[int, int, Item]  # (prio,counter,Item)


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
    del flow_rates[node]
    del graph[node]


def simpflify_graph(graph: Graph, weights: Weights, flow_rates: FlowRates, start: Node, limit: int) -> list[PrioItem]:
    # delete zero flow rate nodes and adjust weights
    nodes = list(graph)
    starts: list[PrioItem] = [(0, 0, (start, limit, 0, set([start])))]
    for node in nodes:
        if node != start and flow_rates[node] == 0:
            remove_node(graph, weights, flow_rates, node)

    if flow_rates[start] == 0:  # remove start at last
        starts = []
        adj = list(graph[start])
        for i, a in enumerate(adj):
            min_left = limit-weights[(start, a)]
            starts.append((0, i, (a, min_left, 0, set())))
        remove_node(graph, weights, flow_rates, start)

    return starts


def estimate_pressure(node: Node, flow: FlowRates, weights: Weights, m: int, opened: set[Node]) -> int:
    # best case for the remaining amount of pressure: (upper bound)
    # - we are at a valve and open it (1 min) -> m-1 min remaining
    # - every next release takes x+1 min (x min travel + 1 min to open)
    # - x is the lowest travel time between all closed valves
    # - we open valves is descending order (flow rate)
    closed_valves = set(flow).difference(opened)  # at least 1
    travel_times = [weights[(e1, e2)] for e1, e2 in combinations(closed_valves | {node}, 2) if (e1, e2) in weights]
    x = 1 if len(travel_times) == 0 else min(travel_times)
    to_open = 1 + ((m-1) // (x+1))
    flow_rates = sorted([flow[n] for n in closed_valves], reverse=True)
    to_open = min(to_open, len(flow_rates))  # cant open more than len(flow_rates) valves
    estimate = sum(flow_rates[i] * (m-1-(x+1)*i) for i in range(to_open))
    return estimate


def max_pressure(graph: Graph, weights: Weights, flow: FlowRates, starts: list[PrioItem]) -> int:
    # prio: highest total pressure comes first -> "best" grows faster and we can skip more candidates
    q: list[PrioItem] = starts  # ( prio, counter, (candidate,minutes_left,sum_press,opened_valves) )
    heapify(q)
    best = 0

    i = 0
    while q:
        _prio, _count, item = heappop(q)
        node, m, p, opened = item

        if node not in opened:
            new_opened = opened | {node}  # open the valve
            new_p = p + (m-1)*flow_rates[node]
            best = max(best, new_p)  # we might have a new best
            if len(new_opened) != len(graph):  # skip if last valve
                # estimate if candidate can ever get better - TODO: necessary here?
                if new_p + estimate_pressure(node, flow, weights, m-1, new_opened) >= best:
                    i += 1
                    heappush(q, (-new_p, i, (node, m-1, new_p, new_opened)))

        # we can keep the valve closed and move on: no "else" here
        for adj in graph[node]:
            w = weights[(node, adj)]  # travel time
            if m - w > 1:  # we need at least 2 min
                # estimate if candidate can ever get better
                if p + estimate_pressure(adj, flow, weights, m-w, opened) >= best:
                    i += 1
                    heappush(q, (-p, i, (adj, m-w, p, opened)))
    print(i)
    return best


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

graph, weights, flow_rates = create_graph(data)
starts = simpflify_graph(graph, weights, flow_rates, "AA", 30)
ans = max_pressure(graph, weights, flow_rates, starts)
print("Part 1:", ans)

# plot_graph(graph, weights)
