import os.path
from timeit import default_timer as timer
from dataclasses import dataclass
from typing import Any


@dataclass
class Node:
    x: int
    steps: int
    prev: Any
    next: Any


def create_linked_list(data: str, key: int) -> tuple[list[Node], Node]:
    split = data.splitlines()
    length = len(split) - 1  # -1 because we will cut a node
    half = (length)/2
    linked_list: list[Node] = []
    prev = None
    zero = None
    for n in split:
        num = int(n)
        steps = (num % length)
        steps = (steps * (key % length)) % length  # part 2
        # take the shorter route
        if steps > half:
            steps = steps - length
        node = Node(num, steps, None, None)
        if prev is not None:
            prev.next = node
            node.prev = prev
        prev = node
        linked_list.append(node)
        if num == 0:
            zero = node

    # make it circular
    linked_list[0].prev = linked_list[-1]
    linked_list[-1].next = linked_list[0]

    assert (zero)
    return linked_list, zero


def mix(node: Node) -> None:
    # do nothing
    if node.x == 0 or node.steps == 0:
        return

    # cut node from list
    node.prev.next = node.next
    node.next.prev = node.prev

    # traverse
    temp = node
    if node.steps > 0:
        for _ in range(node.steps):
            temp = temp.next
    else:  # steps < 0
        # one more step so we can put node in front of temp
        # instead of behind and reuse logic from forward traversing
        for _ in range(abs(node.steps)+1):
            temp = temp.prev

    # put node in front of temp
    node.prev = temp
    node.next = temp.next
    temp.next = node
    node.next.prev = node


def grove_coordinates(linked_list: list[Node], zero: Node, runs: int = 1, key: int = 1) -> int:
    length = len(linked_list)

    # mixing
    for _ in range(runs):
        for node in linked_list:
            mix(node)

    # calc coordinates
    res = []
    steps = 1_000 % length
    for _ in range(3):
        for _ in range(steps):
            zero = zero.next
        res.append(zero.x * key)

    return sum(res)


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

start = timer()

linked_list, zero = create_linked_list(data, 1)
linked_list2, zero2 = create_linked_list(data, 811589153)

p1 = grove_coordinates(linked_list, zero,)
p2 = grove_coordinates(linked_list2, zero2, 10, 811589153)
print("Part 1:", p1)
print("Part 2:", p2)


end = timer()
print("time:", end - start)
