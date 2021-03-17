#### level 3 - 1/3
'''
Doomsday Fuel
=============

Making fuel for the LAMBCHOP's reactor core is a tricky process because of the exotic matter involved. It starts as raw ore, then during processing, begins randomly changing between forms, eventually reaching a stable form. There may be multiple stable forms that a sample could ultimately reach, not all of which are useful as fuel.

Commander Lambda has tasked you to help the scientists increase fuel creation efficiency by predicting the end state of a given ore sample. You have carefully studied the different structures that the ore can take and which transitions it undergoes. It appears that, while random, the probability of each structure transforming is fixed. That is, each time the ore is in 1 state, it has the same probabilities of entering the next state (which might be the same state).  You have recorded the observed transitions in a matrix. The others in the lab have hypothesized more exotic forms that the ore can become, but you haven't seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly.

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

Languages
=========

To provide a Java solution, edit Solution.java
To provide a Python solution, edit solution.py

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
Output:
    [7, 6, 8, 21]

Input:
solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    [0, 3, 2, 9, 14]
'''
def normalize(t):
    from copy import deepcopy
    m = deepcopy(t)
    termState = list()
    for rid, row in enumerate(m):
        s = sum(row)
        if s:
            for i, e in enumerate(row):
                row[i] = e/float(s)
        else:
            termState.append(rid)
            row[rid] = 1
    return m, termState

def solution(m):
    from fractions import Fraction, gcd
    from copy import deepcopy
    from functools import reduce
    # def normalize(m):
    #     t = []
    #     for rid, row in enumerate(m):
    #         s = sum(row)
    #         if s:
    #             r = [Fraction(e, s) for e in row]
    #         else:
    #             r = [0 for e in row]
    #             r[rid] = 1
    #         t.append(r)
    #     return t
    def dot(a, b):
        return sum(map(lambda x: x[0]*x[1], zip(a,b)))
    def cols(m):
        return [[r[i] for r in m] for i in range(len(m))]
    def matmul(m, n):
        res = []
        for row in m:
            r = list()
            for col in cols(n):
                r.append(dot(row, col))
            res.append(r)
        return res
    def sPk(s, m, k):
        s_ = [deepcopy(s)]
        for i in range(k):
            s_ = matmul(s_, m)
        return s_
    def lcm(a, b):
        return abs(a*b)//gcd(a,b)

    P, termStates = normalize(m)
    s0 = [1] + [0 for e in range(len(m)-1)]
    max_iter = 1000
    fres = sPk(s0, P, max_iter)[0]
    fres = [Fraction(e).limit_denominator(65535) for e in fres]
    resStates = [fres[i] for i in termStates]
    denoms = [e.denominator for e in resStates]
    commonDenom = reduce(lcm, denoms)
    res = [e.numerator*(commonDenom/e.denominator) for e in resStates] + [commonDenom]
    return res

if __name__ == '__main__':
    import numpy as np
    from scipy import linalg
    t1 = [
        [0, 1, 0, 0, 0, 1],  # s0, the initial state, goes to s1 and s5 with equal probability
        [4, 0, 0, 3, 2, 0],  # s1 can become s0, s3, or s4, but with different probabilities
        [0, 0, 0, 0, 0, 0],  # s2 is terminal, and unreachable (never observed in practice)
        [0, 0, 0, 0, 0, 0],  # s3 is terminal
        [0, 0, 0, 0, 0, 0],  # s4 is terminal
        [0, 0, 0, 0, 0, 0],  # s5 is terminal
    ]
    t2 = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]
    T = normalize(t1)
    P = np.array(T)
    dim = P.shape[0]
    s0 = np.hstack([[1], np.zeros(dim-1)])
    # print(s0@np.linalg.matrix_power(P, 1000))
    print(solution(t1))
    print(solution(t2))