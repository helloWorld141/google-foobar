### level 5 - 1/1 ###
'''
Expanding Nebula
================

You've escaped Commander Lambda's exploding space station along with numerous escape pods full of bunnies. But -- oh no! -- one of the escape pods has flown into a nearby nebula, causing you to lose track of it. You start monitoring the nebula, but unfortunately, just a moment too late to find where the pod went. However, you do find that the gas of the steadily expanding nebula follows a simple pattern, meaning that you should be able to determine the previous state of the gas and narrow down where you might find the pod.

From the scans of the nebula, you have found that it is very flat and distributed in distinct patches, so you can model it as a 2D grid. You find that the current existence of gas in a cell of the grid is determined exactly by its 4 nearby cells, specifically, (1) that cell, (2) the cell below it, (3) the cell to the right of it, and (4) the cell below and to the right of it. If, in the current state, exactly 1 of those 4 cells in the 2x2 block has gas, then it will also have gas in the next state. Otherwise, the cell will be empty in the next state.

For example, let's say the previous state of the grid (p) was:
.O..
..O.
...O
O...

To see how this grid will change to become the current grid (c) over the next time step, consider the 2x2 blocks of cells around each cell.  Of the 2x2 block of [p[0][0], p[0][1], p[1][0], p[1][1]], only p[0][1] has gas in it, which means this 2x2 block would become cell c[0][0] with gas in the next time step:
.O -> O
..

Likewise, in the next 2x2 block to the right consisting of [p[0][1], p[0][2], p[1][1], p[1][2]], two of the containing cells have gas, so in the next state of the grid, c[0][1] will NOT have gas:
O. -> .
.O

Following this pattern to its conclusion, from the previous state p, the current state of the grid c will be:
O.O
.O.
O.O

Note that the resulting output will have 1 fewer row and column, since the bottom and rightmost cells do not have a cell below and to the right of them, respectively.

Write a function solution(g) where g is an array of array of bools saying whether there is gas in each cell (the current scan of the nebula), and return an int with the number of possible previous states that could have resulted in that grid after 1 time step.  For instance, if the function were given the current state c above, it would deduce that the possible previous states were p (given above) as well as its horizontal and vertical reflections, and would return 4. The width of the grid will be between 3 and 50 inclusive, and the height of the grid will be between 3 and 9 inclusive.  The solution will always be less than one billion (10^9).

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
solution.solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]])
Output:
    11567

Input:
solution.solution([[True, False, True], [False, True, False], [True, False, True]])
Output:
    4

Input:
solution.solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]])
Output:
    254
'''
def setBit(b, k):
    return b | (1<<k)
def getBit(b, k):
    return (b>>k) & 1
def tto(x, y, c):
    return x*c+y
def ott(pos, c):
    return (pos%c, pos/c)

def evolve(p, r, c):
    windows = [(0,0), (0,1), (1,0), (1,1)]
    def checkWindow(p, i, j):
        coords = [(i+x, j+y) for x,y in windows]
        values = [getBit(p, tto(coord[0], coord[1], c)) for coord in coords]
        return values.count(1) == 1
    res = 0
    for i in range(r-1):
        for j in range(c-1):
            if checkWindow(p, i, j):
                res = setBit(res, tto(i, j, c-1))
    return res

def isPrev(p, state, r, c):
    state_ = evolve(p, r, c)
    return state == state_

def matToBin(c):
    bin_str = ''.join([''.join([str(int(i)) for i in row]) for row in c])
    return int(bin_str, 2)
def binToMat(b, n, m):
    mat = list()
    bin_str = bin(b)[2:]
    bin_str = '0'*(n*m - len(bin_str)) + bin_str
    for i in range(n):
        row = bin_str[i*m: (i+1)*m]
        row = [c == '1' for c in row]
        mat.append(row)
    return mat

def exaustedSearch(dest):
    n = len(dest)+1
    m = len(dest[0])+1
    count = 0
    dest_bin = matToBin(dest)
    for i in range(2**(n*m)):
        if isPrev(i, dest_bin, n, m): count += 1
    return count

def solution(g):
    return exaustedSearch(g)

if __name__=='__main__':
    tests = [
        [[True, False, True], [False, True, False], [True, False, True]], # expected 4

        [[True, False, True, False, False, True], [True, False, True, False, False, False],
         [True, True, True, False, False, False], [True, False, True, False, False, False]],  #

        [[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False],
         [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False],
         [True, False, True, False, False, True, True, True]], # expected 254

        [[True, True, False, True, False, True, False, True, True, False],
         [True, True, False, False, False, False, True, True, True, False],
         [True, True, False, False, False, False, False, False, False, True],
         [False, True, False, False, False, False, True, True, False, False]], # expected 11567
    ]

    ### verify a solution ###
    p = [
        [False, True, False, False],
        [False, False, True, False],
        [False, False, False, True],
        [True, False, False, False]
    ]
    p_bin = matToBin(p)
    r = len(p)
    c = len(p[0])
    dest = matToBin(tests[0])
    print(isPrev(p_bin, dest, r, c))
    for t in tests:
        print(solution(t))