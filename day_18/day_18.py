def coord_area(vertices):
    # shoelace formula
    coord_area = 0 
    N = len(vertices)
    for i in range(N):
        i1, j1 = vertices[i]
        i2, j2 = vertices[(i+1)%N]

        coord_area += i1*j2 - i2*j1
    return abs(coord_area)/2

def process_turns(data):
    new = []
    for k, (dir, n) in enumerate(data):
        next_dir, _ = data[(k+1)%len(data)]
        if (next_dir-dir)%4 == 1:
            #right turn
            new.append((dir, n, 'R'))
        elif (next_dir-dir)%4 == 3:
            #left turn
            new.append((dir, n, 'L'))
    return new

def calculate_area(data, clockwise=True):
    data = process_turns(data)
    vertices = [(0,0)]
    prev_turn = -1
    for dir, n, turn in data:
        # there are 2 types of turns: inside and outside
        # depending on the direction you traverse the path
        # their effect is differnt but say we go anti-clockwise
        # outside turns are right turns, inside turns are left turns
        # inside turns add 1 to length of perimeter when counting the #
        # outside turns don't
        # also if we turn outside twice then we lose 2 steps
        i,j = vertices[-1] # last vertex
        check = 'R' if clockwise else 'L'
        add = n+1
        if prev_turn == check:
            add -= 1
        if turn == check:
            add -= 1
        match dir:
            case 0:
                # right
                vertices.append((i,j+add))
            case 1:
                # down
                vertices.append((i+add,j))
            case 2:
                # left
                vertices.append((i,j-add))
            case 3:
                # up
                vertices.append((i-add,j))
        prev_turn = turn
    return int(coord_area(vertices))



DIR_TO_NUM = {'R':0, 'D':1, 'L':2, 'U':3}
with open('input.txt') as f:
    data_1 = []
    data_2 = []
    for line in f:
        dir, n, colour = line.strip().split()
        # Part 1 data
        data_1.append((DIR_TO_NUM[dir], int(n)))
        # Part 2 data
        data_2.append((int(colour[-2]), int(colour[2:-2], 16)))

    print(f"Part 1: {calculate_area(data_1, clockwise=False)}")
    print(f"Part 2: {calculate_area(data_2, clockwise=False)}")

