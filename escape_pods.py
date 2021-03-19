### level 4 - 2/2 ###
'''
Escape Pods
===========

You've blown up the LAMBCHOP doomsday device and relieved the bunnies of their work duries -- and now you need to escape from the space station as quickly and as orderly as possible! The bunnies have all gathered in various locations throughout the station, and need to make their way towards the seemingly endless amount of escape pods positioned in other parts of the station. You need to get the numerous bunnies through the various rooms to the escape pods. Unfortunately, the corridors between the rooms can only fit so many bunnies at a time. What's more, many of the corridors were resized to accommodate the LAMBCHOP, so they vary in how many bunnies can move through them at a time.

Given the starting room numbers of the groups of bunnies, the room numbers of the escape pods, and how many bunnies can fit through at a time in each direction of every corridor in between, figure out how many bunnies can safely make it to the escape pods at a time at peak.

Write a function solution(entrances, exits, path) that takes an array of integers denoting where the groups of gathered bunnies are, an array of integers denoting where the escape pods are located, and an array of an array of integers of the corridors, returning the total number of bunnies that can get through at each time step as an int. The entrances and exits are disjoint and thus will never overlap. The path element path[A][B] = C describes that the corridor going from A to B can fit C bunnies at each time step.  There are at most 50 rooms connected by the corridors and at most 2000000 bunnies that will fit at a time.

For example, if you have:
entrances = [0, 1]
exits = [4, 5]
path = [
  [0, 0, 4, 6, 0, 0],  # Room 0: Bunnies
  [0, 0, 5, 2, 0, 0],  # Room 1: Bunnies
  [0, 0, 0, 0, 4, 4],  # Room 2: Intermediate room
  [0, 0, 0, 0, 6, 6],  # Room 3: Intermediate room
  [0, 0, 0, 0, 0, 0],  # Room 4: Escape pods
  [0, 0, 0, 0, 0, 0],  # Room 5: Escape pods
]

Then in each time step, the following might happen:
0 sends 4/4 bunnies to 2 and 6/6 bunnies to 3
1 sends 4/5 bunnies to 2 and 2/2 bunnies to 3
2 sends 4/4 bunnies to 4 and 4/4 bunnies to 5
3 sends 4/6 bunnies to 4 and 4/6 bunnies to 5

So, in total, 16 bunnies could make it to the escape pods at 4 and 5 at each time step.  (Note that in this example, room 3 could have sent any variation of 8 bunnies to 4 and 5, such as 2/6 and 6/6, but the final solution remains the same.)

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
solution.solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]])
Output:
    6

Input:
solution.solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
Output:
    16
'''

MAX_FLOW = 2e+6
def col(matrix, c):
    return [row[c] for row in matrix]

def findAugmentedPath(src, sink, c, f):
    from collections import deque
    def constructPath(path, dest):
        p = list()
        cur = dest
        while path[cur][0] != cur:
            origin, flow = path[cur]
            p.append((origin, cur, flow))
            cur = path[cur][0]
        return p[::-1]
    def updateFlow(f, p):
        bottleNeck = min(p, key=lambda x: x[-1])[-1]
        for origin, cur, _ in p:
            f[origin][cur] += bottleNeck
            if f[origin][cur] > c[origin][cur]: ## if overflow
                f[cur][origin] += (c[origin][cur] - f[origin][cur]) # go to reversed edge
                f[origin][cur] = c[origin][cur]

    q = deque()
    path = dict()
    for s in src:
        q.append((s, s, MAX_FLOW))
    while q:
        origin, cur, flow = q.popleft()
        path[cur] = (origin, flow)
        if cur in sink:
            p = constructPath(path, cur)
            updateFlow(f, p)
            return p
        positiveOut = [(cur, idx, c[cur][idx] - flow) for idx, flow in enumerate(f[cur]) if c[cur][idx]-flow] # get outgoing edges with positive residual
        negativeFlow = [(cur, idx, flow) for idx, flow in enumerate(col(f, cur)) if flow] # get ingoing edge with positive flow
        neighbors = positiveOut + negativeFlow
        for neighbor in neighbors:
            if neighbor[1] not in path:
                q.append(neighbor)

def calculateMaxSink(f, sinks):
    res = 0
    for row in f:
        res += sum([e for idx, e in enumerate(row) if idx in sinks])
    return res

def solution(entrances, exits, path):
    n = len(path)
    f = [[0 for i in range(n)] for i in range(n)] # keep track of current flow through each edge
    p = findAugmentedPath(entrances, exits, path, f)
    while p:
        p = findAugmentedPath(entrances, exits, path, f)
    res = calculateMaxSink(f, exits)
    return res

if __name__=='__main__':
    tests = [
        [
            [0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]
        ], # expected 6
        [
            [0, 1],
            [4, 5],
            [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        ], # expected 16
        [
            [0],
            [5],
            [
                [0, 10, 10, 0, 0, 0],
                [0, 0, 2, 4, 8, 0],
                [0, 0, 0, 0, 9, 0],
                [0, 0, 0, 0, 0, 10],
                [0, 0, 0, 6, 0, 10],
                [0, 0, 0, 0, 0, 0]
            ]
        ], # expected 19
    ]
    for t in tests:
        res = solution(*t)
        print(res)