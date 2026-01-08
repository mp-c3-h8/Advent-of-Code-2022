import os.path
import re
import numpy as np
from numpy.typing import NDArray
from timeit import default_timer as timer
from z3 import IntVector, Sum, Optimize
from math import prod


def parse_input(data: str) -> list[NDArray]:
    res = []
    for line in data.splitlines():
        coeff = np.zeros((3, 4))
        idx, a1, a2, a3, b3, a4, c4 = re.findall(r"\d+", line)
        coeff[0, 0] = a1
        coeff[0, 1] = a2
        coeff[0, 2] = a3
        coeff[0, 3] = a4
        coeff[1, 2] = b3
        coeff[2, 3] = c4
        res.append(coeff)
    return res


def objective(x, T: int):
    return Sum((T-k-1)*x[k] for k in range(T-1))


def cost(X, blue, r: int, t: int):
    return Sum(b * X[k][t-1]for k in range(4) if (b := int(blue[r, k])) != 0)


def ineq_m_r_i(X, blue, r_start: int, r: int, t: int, T: int):
    s1 = r_start*t
    s2 = Sum((t-k)*X[r][k-1] for k in range(1, t))
    s3 = Sum(cost(X, blue, r, k) for k in range(1, t+2) if k <= T)
    return s1+s2-s3 >= 0


def solution(s) -> int:
    return -s.model().evaluate(s.objectives()[0]).as_long()


def solve_with_z3(blue, T: int) -> int:

    R = [0, 1, 2]  # robot indices
    R_start = [1, 0, 0]  # starting robots

    X = [IntVector('x%s' % i, T) for i in "ABCD"]

    s = Optimize()

    # m_r_i
    for t in range(1, T+1):
        for r, r_start in zip(R, R_start):
            s.add(ineq_m_r_i(X, blue, r_start, r, t, T))

    # f_i
    for t in range(T):
        add = Sum(X[k][t] for k in range(4)) <= 1
        s.add(add)

    # binary
    for X_r in X:
        for x_r_i in X_r:
            s.add(x_r_i >= 0)
            s.add(x_r_i <= 1)

    # objective
    c = objective(X[-1], T)

    # solve
    s.maximize(c)
    assert(repr(s.check()) == "sat")

    return solution(s)


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

start = timer()

blueprints = parse_input(data)

blueprints = parse_input(data)
print("Part 1:", sum(i*solve_with_z3(blue, 24) for i, blue in enumerate(blueprints, 1)))
print("Part 2:", prod(solve_with_z3(blue, 32) for blue in blueprints[:3]))


end = timer()
print("time:", end - start)
