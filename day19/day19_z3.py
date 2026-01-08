import os.path
import re
from timeit import default_timer as timer
from z3 import IntVector, Sum, Optimize
from math import prod
from itertools import chain


def parse_input(data: str) -> list[list[int]]:
    res = []
    for line in data.splitlines():
        coeff = [[0]*4 for _ in range(4)]
        idx, a1, a2, a3, b3, a4, c4 = map(int, re.findall(r"\d+", line))
        coeff[0][0] = a1
        coeff[0][1] = a2
        coeff[0][2] = a3
        coeff[0][3] = a4
        coeff[1][2] = b3
        coeff[2][3] = c4
        res.append(coeff)
    return res


def objective(x, T: int):
    return Sum((T-k-1)*x[k] for k in range(T-1))


def cost(X, robot_costs, r: int, t: int):
    return Sum(robot_costs[r][k] * X[k][t-1]for k in range(4))


def ineq_m_r_i(X, robot_costs, r_start: int, r: int, t: int, T: int):
    s1 = r_start*t  # starting robots gain
    s2 = Sum((t-k)*X[r][k-1] for k in range(1, t))  # built robots gain
    s3 = Sum(cost(X, robot_costs, r, k) for k in range(1, t+2) if k <= T)  # costs
    return s1+s2-s3 >= 0


def create_model(T: int, robot_costs):

    R = [0, 1, 2]  # robot indices
    R_start = [1, 0, 0]  # starting robots

    X = [IntVector('x%s' % i, T) for i in "ABCD"]  # 4xT variables
    s = Optimize()

    # m_r_i
    for t in range(1, T+1):
        for r, r_start in zip(R, R_start):
            s.add(ineq_m_r_i(X, robot_costs, r_start, r, t, T))

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
    s.maximize(c)

    return s


def solve_with_z3(s, blue, robot_costs) -> int:

    # set initial state (robot costs)
    s.push()
    for var, val in zip(chain.from_iterable(robot_costs), chain.from_iterable(blue)):
        s.add(var == val)
        # s.set_initial_value(var,val) #doesnt work

    # solver
    assert (repr(s.check()) == "sat")
    res = -s.model().evaluate(s.objectives()[0]).as_long()  # somehow its negative...bug?
    s.pop()

    return res


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

start = timer()

blueprints = parse_input(data)  # actual robot costs
RC = [IntVector('c%s' % i, 4) for i in "ABC"]  # 3x4 robot cost variables
model = create_model(24, RC)
model2 = create_model(32, RC)

blueprints = parse_input(data)
print("Part 1:", sum(i*solve_with_z3(model, blue, RC) for i, blue in enumerate(blueprints, 1)))
print("Part 2:", prod(solve_with_z3(model2, blue, RC) for blue in blueprints[:3]))


end = timer()
print("time:", end - start)
