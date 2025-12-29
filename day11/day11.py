import os.path
from dataclasses import dataclass, field
from operator import add, mul, pow
from typing import Callable, ClassVar

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

OP = {"+": add, "*": mul}


@dataclass(slots=True)
class Monkey:
    mod: ClassVar[int] = 1
    id: int
    inspect_operation: Callable[[int, int], int]
    inspect_operand: int
    test_divisor: int
    test_true: int
    test_false: int
    items: list[int] = field(default_factory=list)
    total_inspects: int = 0

    def add_item(self, item: int) -> None:
        self.items.append(item)

    def play(self, bored_level: int) -> list[tuple[int, int]]:  # (item,to_monkey)
        res = []
        self.inspect_items()
        if bored_level > 1:
            self.bored(bored_level)
        self.prune_items()  # important for p2 since numbers grow fast
        for item in self.items:
            if self.test_item(item):
                res.append((item, self.test_true))
            else:
                res.append((item, self.test_false))
        self.items = []
        return res

    def inspect_items(self) -> None:
        self.total_inspects += len(self.items)
        self.items = [self.inspect_operation(item, self.inspect_operand) for item in self.items]

    def bored(self, level: int) -> None:
        self.items = [item // level for item in self.items]

    def test_item(self, item: int) -> bool:
        return item % self.test_divisor == 0

    def prune_items(self) -> None:
        self.items = [item % Monkey.mod for item in self.items]


def create_monkeys(data: str) -> dict[int, Monkey]:
    monkeys_str = data.split("\n\n")
    monkeys: dict[int, Monkey] = {}

    for i, monkey_str in enumerate(monkeys_str):
        monkey_lines = monkey_str.splitlines()
        items_str = monkey_lines[1].split(": ", 1)[1]
        op_split = monkey_lines[2].split(" ")
        if op_split[-1] == "old":  # old * old
            inspect_operation = pow
            inspect_operand = 2
        else:
            inspect_operation = OP[op_split[-2]]
            inspect_operand = int(op_split[-1])
        test_divisor = int(monkey_lines[3].split(" ")[-1])
        test_true = int(monkey_lines[4].split(" ")[-1])
        test_false = int(monkey_lines[5].split(" ")[-1])

        monkey = Monkey(i, inspect_operation, inspect_operand, test_divisor, test_true, test_false)
        # https://en.wikipedia.org/wiki/Chinese_remainder_theorem
        # all divisors are prime
        Monkey.mod *= test_divisor
        for item_str in items_str.split(", "):
            monkey.add_item(int(item_str))
        monkeys[i] = monkey
    return monkeys


def play_a_round(monkeys: dict[int, Monkey], bored_level: int) -> None:
    for monkey in monkeys.values():
        throws = monkey.play(bored_level)
        for (item, to_monkey) in throws:
            monkeys[to_monkey].add_item(item)


def monkey_business(monkeys: dict[int, Monkey], bored_level: int, rounds: int) -> int:
    for _ in range(rounds):
        play_a_round(monkeys, bored_level)
    activity = sorted([monkey.total_inspects for monkey in monkeys.values()])
    return activity[-1]*activity[-2]


data = open(input_path).read()
monkeys = create_monkeys(data)
print("Part 1:", monkey_business(monkeys, 3, 20))

monkeys = create_monkeys(data)
print("Part 2:", monkey_business(monkeys, 1, 10000))
