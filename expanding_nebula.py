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
def setBit(b, k, l):
    k = l-k-1
    return b | (1<<k)
def unsetBit(b, k, l):
    k = l-k-1
    return b & ~(1<<k)
def setBits(b, ks, l):
    for k in ks:
        b = setBit(b, k, l)
    return b
def unsetBits(b, ks, l):
    for k in ks:
        b = unsetBit(b, k, l)
    return b
def getBit(b, k, l):
    k = l-k-1
    return (b>>k) & 1
def tto(x, y, c):
    return x*c+y
def ott(pos, c):
    return (pos/c, pos%c)
def bin_to_rows(b, c, expected_r):
    res = list()
    while b:
        res.append(b%(1<<c))
        b = b/(1<<c)
    n = len(res)
    for i in range(expected_r-n):
        res.append(0)
    return res[::-1]

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

def getWindow(cur, pos, r, c):
    l = r*c
    offsets = [(0,0), (0,1), (1,0), (1,1)]
    x, y = ott(pos, c)
    idx = [tto(x+dx, y+dy, c) for dx, dy in offsets]
    return {i: getBit(cur, i, l) for i in idx}


def generateState(pos, cur, fixed, dest, r, c, res): # r, c is dimesions of dest, pos is based on cur dimension
    from itertools import combinations
    if pos == (r+1)*(c+1): ## done constructing cur
        # print(binToMat(cur, r+1, c+1))
        res.append(cur)
        return 1
    if pos % (c+1) == c or pos / (c+1) == r: # pos in last row or last column of cur
        # do nothing
        return generateState(pos+1, cur, fixed, dest, r, c, res)

    l = (r+1)*(c+1)
    dest_x, dest_y = ott(pos, c+1)
    dest_pos = tto(dest_x, dest_y, c)
    b = getBit(dest, dest_pos, r*c)
    windows = getWindow(cur, pos, r+1, c+1)
    free = [k for k in windows.keys() if not getBit(fixed, k, l)] # free cell MUST be 0
    # fixed the current examined window
    fixed = setBits(fixed, windows.keys(), l)
    count1 = windows.values().count(1)
    count = 0 # count the number of satisfied prev states
    if count1 == 0:
        if b == 1: # we need a 1 somewhere, nBranch == len(free)
            for i in free:
                cur = setBit(cur, i, l)
                count += generateState(pos+1, cur, fixed, dest, r, c, res)
                cur = unsetBit(cur, i, l)
        else: # we need all 0s or at least 2 1s
            if len(free) == 1: # can't do shit, just move on
                pass
            elif len(free) == 2: # either both are 0s, or both are 1s
                cur = setBits(cur, free, l)
                count += generateState(pos+1, cur, fixed, dest, r, c, res) # both are 1s
                cur = unsetBits(cur, free, l)
            elif len(free) == 4: # only happend at the first position, most complicated
                # there are fucking 11 branches here
                toSets = list(combinations(free, 4)) + list(combinations(free, 3)) + list(combinations(free, 2))
                for s in toSets:
                    cur = setBits(cur, s, l)
                    count += generateState(pos+1, cur, fixed, dest, r, c, res)
                    cur = unsetBits(cur, s, l)
            else: # not even happening
                pass
            # set all to zeros, since it happend in every case of len(free)
            count += generateState(pos+1, cur, fixed, dest, r, c, res)  # set all free to zeros, no matter how many free
    elif count1 == 1:
        if b == 1: # that's settled, bit 1 must be already fixed, other bits must remain zero, nothing to do here
            count += generateState(pos+1, cur, fixed, dest, r, c, res) # set all free to zeros, no matter how many free
        else: #
            if len(free) == 1:
                cur = setBits(cur, free, l)
                count += generateState(pos+1, cur, fixed, dest, r, c, res) # set all free to zeros, no matter how many free
                cur = unsetBits(cur, free, l)
            elif len(free) == 2: # set each bit, or set both bits
                toSets = list(combinations(free, 2)) + list(combinations(free, 1))
                for s in toSets:
                    cur = setBits(cur, s, l)
                    count += generateState(pos+1, cur, fixed, dest, r, c, res)
                    cur = unsetBits(cur, s, l)
            else: # cant have 3 or 4 free here
                pass
    else: # count1 > 1
        if b == 1: # this is a dead end
            pass
        else: # this is already satisfied, the free bits can be free
            # 2**free branches here
            toSets = list()
            for i in range(len(free)+1):
                toSets.extend(list(combinations(free, i)))
            toSets = reversed(toSets)
            for s in toSets:
                cur = setBits(cur, s, l)
                count += generateState(pos+1, cur, fixed, dest, r, c, res)
                cur = unsetBits(cur, s, l)
    return count

def getCol(mat, i):
    return [row[i] for row in mat]
def transpose(g):
    m = len(g[0])
    return [getCol(g, i) for i in range(m)]
def solution(g):
    from collections import defaultdict
    g = transpose(g)
    n = len(g)
    m = len(g[0])
    dest = matToBin(g)
    rows = bin_to_rows(dest, m, n)
    prev = {i: 1 for i in range(1<<(m+1))}  # key: the second row of the preimages of a dest's row
                                            # value: the number of possibilities to reach key, following all the rows above its post-image in dest
    for row in rows:
        preimages = list()
        generateState(0, 0, 0, row, 1, m, preimages)
        preimages_rows = [bin_to_rows(pre, m+1, 2) for pre in preimages]
        count = defaultdict(int)
        for preimage in preimages_rows:
            if preimage[0] in prev:
                count[preimage[1]] += prev[preimage[0]]
        prev = count
        # print(preimages)
        # print(binToMat(preimages[0], 2, m+1)
    return sum(prev.values())

### experiment ###

def evolve_row(r1, r2, c):
    c1 = (r1 & ~(1<<(c-1)))<<1
    c2 = (r2 & ~(1<<(c-1)))<<1
    return ((c1&~c2&~r1&~r2) | (~c1&c2&~r1&~r2) | (~c1&~c2&r1&~r2) | (~c1&~c2&~r1&r2)) >> 1

def evolve(p, r, c): # r,c are dimensions of p
    windows = [(0,0), (0,1), (1,0), (1,1)]
    def checkWindow(p, i, j):
        coords = [(i+x, j+y) for x,y in windows]
        values = [getBit(p, tto(coord[0], coord[1], c), r*c) for coord in coords]
        return values.count(1) == 1
    res = 0
    for i in range(r-1):
        for j in range(c-1):
            if checkWindow(p, i, j):
                res = setBit(res, tto(i, j, c-1), (r-1)*(c-1))
    return res

def isPrev(p, state, r, c): # r,c are dimensions of p (bigger than state's)
    state_ = evolve(p, r, c)
    return state == state_

def countStates(dest, r, c): # r, c is dimensions of dest
    cur = 0
    fixed = 0
    pos = 0
    res = list()
    count = generateState(pos, cur, fixed, dest, r, c, res)
    print(res)
    return count

def brute_force(g):
    n = len(g)
    m = len(g[0])
    dest = matToBin(g)
    return countStates(dest, n, m)

def vsplitMat(mat, split):
    return [row[split] for row in mat]

def deriveMat(mat):
    n = len(mat)
    m = len(mat[0])
    split = (m+1)/2
    left = vsplitMat(mat, slice(split))
    right = vsplitMat(mat, slice(split-1, None))
    middle = vsplitMat(mat, slice(split-1, split))
    return left, right, middle

if __name__=='__main__':
    tests = [
        [[True, False, True],
         [False, True, False],
         [True, False, True]], # expected 4
        #
        # [[True, False, True],
        #  [False, True, False],
        #  [False, False, False]],  # expected 4
        #
        # [[True,  True, True, True],
        #  [False, False, False, False],
        #  [False, True, True, False]],  # expected 4

        # [[True, True],
        #  [False, False],
        #  [False, True]],
        #
        # [[True, True],
        #  [False, False],
        #  [True, True]]
        #
        # [[True, False, True],
        #  [False, True, True],
        #  [False, False, True]],
        #
        # [[True, False, True]],
        # [
        #     [True],
        #     [False],
        #     [False],
        # ],
        # [
        #     [True, True],
        #     [False, True]
        # ],
        #
        # [
        #     [True, False],
        #     [False, True]
        # ],
        # [
        #     [True, False],
        #     [True, True]
        # ],
        # [
        #     [False, False],
        #     [False, True]
        # ],
        # [
        #     [True, False],
        #     [True, True]
        # ],

        [[True, False, True, False, False, True], [True, False, True, False, False, False],
         [True, True, True, False, False, False], [True, False, True, False, False, False]],  # expected: 1109

        [[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False],
         [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False],
         [True, False, True, False, False, True, True, True]], # expected 254

        [[True, True, False, True, False, True, False, True, True, False],
         [True, True, False, False, False, False, True, True, True, False],
         [True, True, False, False, False, False, False, False, False, True],
         [False, True, False, False, False, False, True, True, False, False]], # expected 11567
    ]

    ### verify a solution ###
    # p = [
    #     [False, True, False, False],
    #     [False, False, True, False],
    #     [False, False, False, True],
    #     [True, False, False, False]
    # ] # known CORRECT
    # p_bin = matToBin(p)
    # r = len(p)
    # c = len(p[0])
    # dest = matToBin(tests[0])
    # print(isPrev(p_bin, dest, r, c))
    #### solve tests #####
    for t in tests:
        print(solution(t))
    #     left, right, mid = deriveMat(t)
    #     print(left)
    #     print(right)
    #     print(mid)
    #
    #     print(solution(left))
    #     print(solution(right))
    #     print(solution(mid))
    #     print('')

    # for i in range(2**4):
    #     n = m = 2
    #     print("Config {0}:".format(i))
    #     print(binToMat(i, n, m))
    #     print("Count = {0}".format(countStates(i, n, m)))
    # print(evolve_row(4,1,3))
    # print(evolve_row(6, 5, 3))
    # print(bin_to_rows(int('101110100', 2), 3, 3))
    # print(transpose([[1,2,3], [4,5,6]]))
