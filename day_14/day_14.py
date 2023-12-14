def in_bounds(pos, bounds):
    i, j = pos
    i_max, j_max = bounds
    return 0 <= i <= i_max and 0 <= j <= j_max

def sort_key(dir):
    if dir == 'N':
        return lambda x: x[0]
    if dir == 'S':
        return lambda x: -x[0]
    if dir == 'W':
        return lambda x: x[1]
    if dir == 'E':
        return lambda x: -x[1]

def roll(moveable, fixed, dir, bounds):
    moveable = sorted(list(moveable), key=sort_key(dir))
    i_max, j_max = bounds
    moves = {'N': (-1,0), 'W': (0,-1), 'S': (1, 0), 'E': (0,1)}
    move = moves[dir]
    #square_fixed = set(fixed)
    stopped = set()
    for rock in moveable:
        i,j = rock
        di, dj = move
        next = (i+di, j+dj)
        while next not in fixed and next not in stopped and in_bounds(next, bounds):
            i, j = next
            next = (i+di, j+dj)
        stopped.add((i,j))
    return stopped

def cycle(moveable, fixed, bounds):
    for dir in ['N','W','S','E']:
        moveable = roll(moveable, fixed, dir, bounds)
    return moveable

def visual(fixed, moveable, bounds):
    moveable = set(moveable)
    i_max, j_max = bounds
    for i in range(i_max+1):
        line = ''
        for j in range(j_max+1):
            if (i,j) in fixed:
                line += '#'
            elif (i,j) in moveable:
                line += 'O'
            else:
                line += '.'
        print(line)
    print('\n')

def hash_points(points):
    h = ''
    for i,j in points:
        h += f"{i},{j},"
    return h

def total_load(moveable, i_max):
    total = 0
    for i,j in moveable:
        total += i_max - i + 1
    return total

with open('input.txt') as f:
    fixed = set()
    moveable = set()
    lines = f.readlines()
    i_max, j_max = len(lines)-1, len(lines[0])-2 # contains \n
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '#':
                fixed.add((i,j))
            elif c == 'O':
                moveable.add((i,j))

    # Part 1
    tilted = roll(moveable, fixed, 'N', (i_max, j_max))
    print(f"Part 1: {total_load(tilted, i_max)}")

    # Part 2
    states = set(hash_points(moveable))
    k = 0
    count = 0
    total_loops = 1_000_000_000
    period = 0
    loop_k = []
    while True:
        k+=1
        moveable = cycle(moveable, fixed,(i_max, j_max))
        if hash_points(moveable) in states:
            states = set()
            loop_k.append(k)
            if count > 1:
                period = loop_k[-1] - loop_k[-2]
                start_bit = loop_k[1] - period
                break
            count += 1
        else:
            states.add(hash_points(moveable))
    
    last_bit = (total_loops - start_bit) % period

    # simulate the necessary stuff
    for i in range(start_bit + last_bit):
        moveable = cycle(moveable, fixed, (i_max, j_max))
    #visual(fixed, moveable, (i_max, j_max))
    print(f"Part 2: {total_load(moveable, i_max)}")
