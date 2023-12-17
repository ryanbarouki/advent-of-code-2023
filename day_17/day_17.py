from queue import PriorityQueue
from collections import defaultdict

def get_left_right(dir):
    if dir[0] != 0: 
        return {(0,1),(0,-1)}
    return {(1,0),(-1,0)}

def get_directions(data_map, state, dir, run, min_run, max_run):
    i,j = state
    dirs = set()
    if run < min_run:
        # can only go forwards
        dirs.add(dir)
    elif min_run <= run < max_run:
        dirs |= get_left_right(dir)
        dirs.add(dir)
    elif run >= max_run:
        dirs |= get_left_right(dir)
    valid = set()
    for d in dirs:
        di,dj = d 
        next = (i+di, j+dj)
        if next in data_map:
            valid.add(d)
    return valid

def dijkstra(data_map, start, end, min_run=0, max_run=3):
    # Dijkstra where 'nodes' are (position, direction, run)
    pq = PriorityQueue()
    pq.put((0, start, (0, 1), 1, [start]))  # dist, pos, dir, run, path
    distances = defaultdict(lambda: float('inf'))

    while not pq.empty():
        dist, pos, dir, run, path = pq.get()
        state = (pos,dir,run) # this is the key point - states are defined as so

        # direction doesn't matter at end
        if pos == end and run >= min_run: 
            return dist, path

        if dist > distances[state]:
            continue

        for d in get_directions(data_map, pos, dir, run, min_run, max_run):
            i, j = pos
            di, dj = d
            neighbor_pos = (i+di, j+dj)
            weight = data_map[neighbor_pos]  
            new_dist = dist + weight
            next_run = run + 1 if d == dir else 1
            new_path = path + [(neighbor_pos,d)]
            neighbor_state = (neighbor_pos,d,next_run)

            if new_dist < distances[neighbor_state]:
                distances[neighbor_state] = new_dist
                pq.put((new_dist, neighbor_pos, d, next_run, new_path))

    return None  # Path not found

def show(data_map, path):
    for p in path:
        pos, dir = p
        if dir == (0,1):
            data_map[pos] = '>'
        elif dir == (0,-1):
            data_map[pos] = '<'
        elif dir == (1,0):
            data_map[pos] = 'v'
        elif dir == (-1,0):
            data_map[pos] = '^'

    for i in range(len(data)):
        line = ''
        for j in range(len(data[i])):
            line += str(data_map[(i,j)])
        print(line)

with open('input.txt') as f:
    data = [[int(c) for c in line.strip()] for line in f]

    # 140 x 140 data
    end = (len(data)-1,len(data[0])-1)

    data_map = {(i,j): data[i][j] for i in range(len(data)) for j in range(len(data[i]))}
    distance_1, _ = dijkstra(data_map, (0,0), end, min_run=0, max_run=3)
    print(f"Part 1: {distance_1}")

    distance_2, path = dijkstra(data_map, (0,0), end, min_run=4, max_run=10)
    print(f"Part 2: {distance_2}")

    #show(data_map, path)

