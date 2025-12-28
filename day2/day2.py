import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()

POINTS = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}
OUTCOME = {"X": 0, "Y": 3, "Z": 6}
LOOSES_AGAINST = {"A": "B", "B": "C", "C": "A"}
WINS_AGAINST = {"A": "C", "B": "A", "C": "B"}


def outcome(opponent, me) -> int:
    p_o, p_me = POINTS[opponent], POINTS[me]
    if p_o == p_me:
        return 3
    if p_o == 1:  # rock
        if p_me == 2:  # paper
            return 6
        return 0
    if p_o == 2:  # paper
        if p_me == 1:  # rock
            return 0
        return 6
    if p_o == 3:  # scissor
        if p_me == 1:  # rock
            return 6
        return 0
    return -1


def choose(opponent, outcome) -> str:
    out = OUTCOME[outcome]
    if out == 3:
        return opponent
    if out == 0:  # need to loose
        return WINS_AGAINST[opponent]
    return LOOSES_AGAINST[opponent]


p1, p2 = 0, 0
for game in data:
    opponent, me = game.split(" ")
    p1 += POINTS[me] + outcome(opponent, me)
    p2 += POINTS[choose(opponent, me)] + OUTCOME[me]


print("Part 1:", p1)
print("Part 2:", p2)
