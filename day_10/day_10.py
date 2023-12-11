from collections import defaultdict
from collections import deque
from functools import reduce

def get_moves(i,j,c,bounds):
    i_max, j_max = bounds
    match c:
        case 'S':
            moves = []
            if i > 0:
                moves.append((-1,0))
            if i < i_max:
                moves.append((1,0))
            if j > 0:
                moves.append((0,-1))
            if j < j_max:
                moves.append((0,1))
            return moves
        case 'F':
            moves = []
            if i < i_max:
                moves.append((1,0))
            if j < j_max:
                moves.append((0,1))
            return moves
        case 'L':
            moves = []
            if i > 0:
                moves.append((-1,0))
            if j < j_max:
                moves.append((0,1))
            return moves
        case 'J':
            moves = []
            if i > 0:
                moves.append((-1,0))
            if j > 0:
                moves.append((0,-1))
            return moves
        case '7':
            moves = []
            if i < i_max:
                moves.append((1,0))
            if j > 0:
                moves.append((0,-1))
            return moves
        case '|':
            moves = []
            if i > 0:
                moves.append((-1,0))
            if i < i_max:
                moves.append((1,0))
            return moves
        case '-':
            moves = []
            if j > 0:
                moves.append((0,-1))
            if j < j_max:
                moves.append((0,1))
            return moves

    return []

def create_adj_map(map, start):
    pipes_after_move = {(0,1): ['-','J','7','S'],
                        (0,-1): ['-','L','F','S'],
                        (-1,0): ['|','7','F','S'],
                        (1,0): ['|','L','J','S']}
    adj_map = defaultdict(lambda: [])
    for i, row in enumerate(map):
        for j, c in enumerate(row):
            for move in get_moves(i, j, c, (len(map)-1, len(row)-1)):
                di, dj = move
                next = map[i+di][j+dj]
                if next in pipes_after_move[move]:
                    adj_map[(i,j)].append((i+di,j+dj))
    return adj_map

    
def dfs(start, adj_map):
    visited = set()
    queue = deque()
    queue.append((start, 0, [start]))

    count = 0
    while len(queue) > 0:
        count += 1
        node, dist, path = queue.pop()
        if node != start:
            visited.add(node)
        if node == start and count > 1:
            return dist, path
        for neighbour in adj_map[node]:
            if neighbour not in visited:
                path.append(neighbour)
                queue.append((neighbour, dist+1, path))

    return -1

def get_neighbours(node, boundary_set, bounds):
    i,j = node
    i_max, j_max = bounds
    possible_moves = set()
    if i < i_max:
        possible_moves.add((i+1,j))
    if i > 0:
        possible_moves.add((i-1,j))
    if j < j_max:
        possible_moves.add((i,j+1))
    if j > 0:
        possible_moves.add((i,j-1))
    moves = filter(lambda x: x not in boundary_set, possible_moves)
    return moves

def bfs(start, boundary_set, bounds):
    visited = set()
    queue = deque()
    queue.append(start)
    visited.add(start)

    while len(queue) > 0:
        node = queue.popleft()

        for neighbour in get_neighbours(node, boundary_set, bounds):
            if neighbour not in visited:
                queue.append(neighbour)
                visited.add(neighbour)

    return visited

def add_to_set(node, sett, path_set, bounds):
    if node not in sett and node not in path_set:
        sett.add(node)
        sett |= bfs(node, path_set, bounds)

def get_right_of_path(path, bounds):
    i_max, j_max = bounds
    right = set()
    path_set = set(path)
    for k, pos in enumerate(path):
        if k < len(path) - 1:
            i,j = pos
            I,J = path[k+1]
            diff = (I-i, J-j)
            match diff:
                case (0,1):
                    # right: (0,1)
                    if I < i_max:
                        add_to_set((I+1,J), right, path_set, bounds)
                        add_to_set((i+1,j), right, path_set, bounds)
                case (0,-1):
                    # left: (0,-1)
                    if I > 0:
                        add_to_set((I-1,J), right, path_set, bounds)
                        add_to_set((i-1,j), right, path_set, bounds)
                case (-1,0):
                    # up: (-1,0)
                    if J < j_max:
                        add_to_set((I,J+1), right, path_set, bounds)
                        add_to_set((i,j+1), right, path_set, bounds)
                case (1,0):
                    # down: (1,0)
                    if J > 0:
                        add_to_set((I,J-1), right, path_set, bounds)
                        add_to_set((i,j-1), right, path_set, bounds)
    return right


with open('input.txt') as f:
    map = []
    start = ()
    for line in f.readlines():
        map.append(line.strip())
    for i, row in enumerate(map):
        for j, c in enumerate(row):
            if c == 'S':
                start = (i,j)

    bounds = (len(map) - 1, len(map[0]) - 1)
    adj_map = create_adj_map(map, start)
    dist, path = dfs(start, adj_map)
    
    # for part 2
    right = get_right_of_path(path, bounds)
    path_set = set(path)

    print(f"Part 1: {int(dist/2)}")

    # for visualisation and part 2
    new_map = [[c for c in row] for row in map]
    for i, line in enumerate(map):
        for j, c in enumerate(line):
            if (i,j) in path_set:
                new_map[i][j] = map[i][j]
            elif (i,j) in right:
                new_map[i][j] = 'R'
            else:
                # This will be everying to the left of the loop by definition
                new_map[i][j] = '.'

    # we either have to count 'R' or '.' depending on visualisation
    to_count = 'R'
    # print the new map to see what's going on
    count = 0
    for line in new_map:
        print("".join(line))
        count += line.count(to_count)

    # we either have to count 'R' or '.' depending on visualisation
    print(f"Part 2: {count}")
