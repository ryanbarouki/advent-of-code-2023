from collections import deque

OUTGOING_DIRS = {'/': {(0,1): [(-1,0)], (0,-1): [(1,0)], (1,0): [(0,-1)], (-1,0): [(0,1)]},
                 '\\': {(0,1): [(1,0)], (0,-1): [(-1,0)], (1,0): [(0,1)], (-1,0): [(0,-1)]},
                 '-': {(0,1): [(0,1)], (0,-1): [(0,-1)], (1,0): [(0,1),(0,-1)], (-1,0): [(0,1),(0,-1)]},
                 '|': {(0,1): [(1,0),(-1,0)], (0,-1): [(1,0),(-1,0)], (1,0): [(1,0)], (-1,0): [(-1,0)]}}

def in_bounds(pos, bounds):
        i_max, j_max = bounds
        i,j = pos
        return 0 <= i <= i_max and 0 <= j <= j_max

def total_energised(data, start_pos, start_dir):
    bounds = (len(data)-1, len(data[0])-1)
    start = (start_pos, start_dir) 
    beams = deque()
    beams.append(start)

    energised = set()
    paths = set() # identified by position and direction
    while len(beams) > 0:
        beam = beams.popleft()
        pos, dir = beam
        i,j = pos
        di, dj = dir
        # stop repeated traversals
        if (i,j,di,dj) in paths:
            continue
        paths.add((i,j,di,dj))
        tile = data[i][j]
        energised.add(pos)

        if tile == '.':
            next = (i+di, j+dj)
            if in_bounds(next, bounds):
                beams.append((next, dir))
        else: 
            next_dirs = OUTGOING_DIRS[tile][dir]
            for next_d in next_dirs:
                di,dj = next_d
                next = (i+di,j+dj)
                if in_bounds(next, bounds):
                    beams.append((next, next_d))
    return len(energised)


with open('input.txt') as f:
    data = [[c for c in line.strip()] for line in f]
    print(f"Part 1 : {total_energised(data, (0,0), (0,1))}")
    num_energised = []
    for i in range(len(data)):
        # its a square
        num_energised.append(total_energised(data, (i,0), (0,1)))
        num_energised.append(total_energised(data, (i,len(data[0])-1), (0,-1)))
        num_energised.append(total_energised(data, (0,i), (1,0)))
        num_energised.append(total_energised(data, (len(data)-1,i), (-1,0)))
    print(f"Part 2: {max(num_energised)}")
            
