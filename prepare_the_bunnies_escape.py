### level 3 - 2/3 ###
"""
Prepare the Bunnies' Escape
===========================

You're awfully close to destroying the LAMBCHOP doomsday device and freeing Commander Lambda's bunny workers, but once they're free of the work duties the bunnies are going to need to escape Lambda's space station via the escape pods as quickly as possible. Unfortunately, the halls of the space station are a maze of corridors and dead ends that will be a deathtrap for the escaping bunnies. Fortunately, Commander Lambda has put you in charge of a remodeling project that will give you the opportunity to make things a little easier for the bunnies. Unfortunately (again), you can't just remove all obstacles between the bunnies and the escape pods - at most you can remove one wall per escape pod path, both to maintain structural integrity of the station and to avoid arousing Commander Lambda's suspicions.

You have maps of parts of the space station, each starting at a work area exit and ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, where 0s are passable space and 1s are impassable walls. The door out of the station is at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1).

Write a function solution(map) that generates the length of the shortest path from the station door to the escape pod, where you are allowed to remove one wall as part of your remodeling plans. The path length is the total number of nodes you pass through, counting both the entrance and exit nodes. The starting and ending positions are always passable (0). The map will always be solvable, though you may or may not need to remove a wall. The height and width of the map can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal moves are allowed.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

Test cases
==========
Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]])
Output:
    7

Input:
solution.solution([[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]])
Output:
    11
"""

def bfs(src, dest, m):
    def isValidCell(x, y, m):
        r = len(m)
        c = len(m[0])
        return x >= 0 and x < r and y >= 0 and y < c
    def neighbors(x, y, m):
        nbs = list()
        offsets = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for dx, dy in offsets:
            if isValidCell(x + dx, y + dy, m):
                nbs.append((x+dx, y+dy))
        return nbs

    from collections import deque
    q = deque()
    visited = [[e == 1 for e in row] for row in m]
    q.append((src, 1))
    visited[src[0]][src[1]] = True
    # for row in visited:
    #     print(row)
    while q:
        cur, steps = q.popleft()
        if cur == dest:
            return steps
        else:
            x, y = cur
            nbs = neighbors(x, y, m)
            # print(nbs)
            for n in nbs:
                if not visited[n[0]][n[1]]:
                    q.append((n, steps+1))
                    visited[n[0]][n[1]] = True
    return 400

def solution(m):
    from copy import deepcopy
    r = len(m)
    c = len(m[0])
    src = (0,0)
    dest = (r-1, c-1)
    min_res = bfs(src, dest, m)
    for i in range(r):
        for j in range(c):
            if m[i][j]:
                m_ = deepcopy(m)
                m_[i][j] = 0
                min_res = min(min_res, bfs(src, dest, m_))
    return min_res

if __name__=="__main__":
    tests = [
        [
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [1, 1, 0, 0],
            [1, 1, 1, 0]
        ],
        [
            [0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0]
        ]
    ]
    for t in tests:
        src = (0,0)
        dest = (len(t)-1, len(t[0])-1)
        print("No removal: {0}".format(bfs(src, dest, t)))
        print("With removal: {0}".format(solution(t)))