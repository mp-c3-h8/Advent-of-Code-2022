import os.path
import re
import numpy as np
from numpy.typing import NDArray
from cvxopt.glpk import ilp
from cvxopt import matrix
from math import prod
from timeit import default_timer as timer

'''
Example:

Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

for T = 4 (unfeasible, but for illustration) and x_R := (x_R^1,...x_R^4), x_R^i in {0,1}
where x_R^i := a robot producing resource R is ready AT THE END of minute i (thus production of robot must start at i-1),
i in {1,2,3,4}, i := END of minute i, resource R in {A,B,C,D} with ore = A, clay = B, obsidian = C, geode = D,
x = (x_A , x_B, x_C, x_D) in {0,1}^16
we get the System

                                      c^T
       maximize    [ 0 0 0 0 | 0 0 0 0 | 0 0 0 0 | 3 2 1 0 ]  *  x    =   3* x_D^1 + 2* x_D^2 + 1* x_D^3

       subject to

                 x_A              x_B                x_C              x_D                      b
       |-------------------|-----------------|-----------------|----------------|            |---|
m_A^1  | 4    4    0    0  |  2   2   0   0  |  3   3   0   0  |  2   2   0   0 |            | 1 |
m_A^2  | 4-1  4    4    0  |  2   2   2   0  |  3   3   3   0  |  2   2   2   0 |            | 2 |  (we start with 1 robot A)
m_A^3  | 4-2  4-1  4    4  |  2   2   2   2  |  3   3   3   3  |  2   2   2   2 |            | 3 |
m_A^4  | 4-3  4-2  4-1  4  |  2   2   2   2  |  3   3   3   3  |  2   2   2   2 |            | 4 |
       --------------------------------------------------------------------------            |---|
m_B^1  | 0    0    0    0  |  0   0   0   0  | 14  14   0   0  |  0   0   0   0 |            | 0 |
m_B^2  | 0    0    0    0  | -1   0   0   0  | 14  14  14   0  |  0   0   0   0 |            | 0 |
m_B^3  | 0    0    0    0  | -2  -1   0   0  | 14  14  14  14  |  0   0   0   0 |            | 0 |
m_B^4  | 0    0    0    0  | -3  -2  -1   0  | 14  14  14  14  |  0   0   0   0 |            | 0 |
       --------------------------------------------------------------------------  *  x  <=  |---|
m_C^1  | 0    0    0    0  |  0   0   0   0  |  0   0   0   0  |  7   7   0   0 |            | 0 |
m_C^2  | 0    0    0    0  |  0   0   0   0  | -1   0   0   0  |  7   7   7   0 |            | 0 |
m_C^3  | 0    0    0    0  |  0   0   0   0  | -2  -1   0   0  |  7   7   7   7 |            | 0 |
m_C^4  | 0    0    0    0  |  0   0   0   0  | -3  -2  -1   0  |  7   7   7   7 |            | 0 |
       --------------------------------------------------------------------------            |---|
f^1    | 1    0    0    0  |  1   0   0   0  |  1   0   0   0  |  1   0   0   0 |            | 1 |
f^2    | 0    1    0    0  |  0   1   0   0  |  0   1   0   0  |  0   1   0   0 |            | 1 | (factory produces one robot at a time)
f^3    | 0    0    1    0  |  0   0   1   0  |  0   0   1   0  |  0   0   1   0 |            | 1 |
f^4    | 0    0    0    1  |  0   0   0   1  |  0   0   0   1  |  0   0   0   1 |            | 1 |
       |-------------------|-----------------|-----------------|----------------|            |---|


to derive the system consider m_R^i := amount of resource R collected AT THE END of minute i:



                 for a new robot at i=2 we need to pay at i=1                           what we already paid
                      ---------------------------------                         ---------------------------------
                      ↓          ↓          ↓         ↓                         ↓          ↓          ↓         ↓
                      ↓          ↓          ↓         ↓                         ↓          ↓          ↓         ↓
m_A^1 =  1  +  (- 4* x_A^2 - 2* x_B^2 - 3* x_C^2 - 2* c_D^2)      +      (- 4* x_A^1 - 2* x_B^1 - 3* x_C^1 - 2* c_D^1)   >=  0

the constant term being our starting robot A. introducing c_R^i := cummulative cost of resource R to have ready robots AT THE END of minute i:

c_A^i =  4*  x_A^i + 2* x_B^i + 3* x_C^i + 2* x_D^i
c_B^i = 14*  x_C^i
c_C^i =  7*  x_D^i
c_D^i =  0

we can write

m_A^1  =  1                                 - (c_A^1 + c_A^2)                   >=  0
m_A^2  =  2 +                     (1*x_A^1) - (c_A^1 + c_A^2 + c_A^3)           >=  0
m_A^3  =  3 +           (1*x_A^2 + 2*x_A^1) - (c_A^1 + c_A^2 + c_A^3 + c_A^4)   >=  0
m_A^4  =  4 + (1*x_A^3 + 2*x_A^2 + 3*x_A^1) - (c_A^1 + c_A^2 + c_A^3 + c_A^4)   >=  0

m_B^i and m_C^i are similar, but without constant term (no starting robots). since no robot needs resource D (geodes) for construction,
inequalities m_D^i are always satisfied, thus we neglect them, i.e.

m_D^3 = (1*x_D^2 + 2*x_D^1)  >=  0    (always true)


f^i takes care of the fact that the factory can only produce one robot at a time:

f^i  =  x_A^i + x_B^i + x_C^i + x_D^i   <=   1


input data for this example: (compare with above matrix)

              r_A   r_B    r_C    r_D
            |-----|-----|-------|-----|        Each ore robot costs 4 ore.
   ore   A  |  4  |  2  |   3   |  2  |        Each clay robot costs 2 ore.
  clay   B  |  0  |  0  |  14   |  0  |        Each obsidian robot costs 3 ore and 14 clay.
  obsi   C  |  0  |  0  |   0   |  7  |        Each geode robot costs 2 ore and 7 obsidian.
 geode   D  |  0  |  0  |   0   |  0  |    <-- geodes are not used for construction (neglect)
            |-------------------------|
'''


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


def block(size: int, val: int) -> NDArray:
    return np.tril(val*np.ones((size, size)), 1)


def gain_block(size: int) -> NDArray:
    res = np.zeros((size, size))
    for j in range(size):
        for i in range(0, j):
            res[j, i] = -j + i
    return res


def rhs(size: int) -> NDArray:
    a = np.array([i+1 for i in range(size)])
    b = np.zeros(2*size)
    c = np.ones(size)
    return np.concatenate((a, b, c))


def objective(size: int) -> NDArray:
    a = np.zeros(3*size)
    b = np.array([-i for i in range(size-1, -1, -1)])
    return np.concatenate((a, b))


def solve(input: NDArray, minutes: int) -> int:
    T = minutes
    A = np.zeros((3*T, 4*T))
    for j, row in enumerate(input):
        for i, c in enumerate(row):
            if c != 0:
                B = block(T, c)
                A[j*T:(j+1)*T, i*T:(i+1)*T] += B

    C = gain_block(T)
    for i in range(3):
        A[i*T:(i+1)*T, i*T:(i+1)*T] += C

    # factory can only build one robot at a time!!!!!
    E = np.eye(T)
    D = np.hstack([E for _ in range(4)])
    A = np.vstack((A, D))

    b = rhs(T)
    c = objective(T)  # negative since linprog minimizes

    (status, x) = ilp(c=matrix(c, tc='d'),
                      G=matrix(A, tc='d'),
                      h=matrix(b, tc='d'),
                      B=set(range(4*T)),
                      options=dict(msg_lev='GLP_MSG_OFF'))
    assert (status == 'optimal')
    return -round(sum(c[i]*x[i] for i in range(3*T, 4*T)))


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
with open(input_path) as f:
    data = f.read()

start = timer()

blueprints = parse_input(data)
print("Part 1:", sum(i*solve(blueprint, 24) for i, blueprint in enumerate(blueprints, 1)))
print("Part 2:", prod(solve(blueprint, 32) for blueprint in blueprints[:3]))

end = timer()
print("time:", end - start)
