from collections import deque
import numpy as np

def get_neighbours(data_map, node):
    i,j = node
    ilen = len(data)
    jlen = len(data[0])
    neighbours = {(i+1,j),(i-1,j),(i,j+1),(i,j-1)}
    accept = set()
    for neighbour in neighbours:
        I,J = neighbour
        wrapped_neighbour = (I%ilen,J%jlen)
        if data_map[wrapped_neighbour] != '#':
            accept.add(neighbour)
    return accept

def bfs(start, data_map, max_steps):
    queue = deque()
    even_visited = set()
    odd_visited = set()
    queue.append((start, 0))
    even_visited.add(start)

    end_of_walk = set()
    while len(queue):
        node, steps = queue.popleft()

        if steps == max_steps:
            continue
            
        for neighbour in get_neighbours(data_map, node):
            visited = even_visited if (steps+1)%2==0 else odd_visited
            if neighbour not in visited:
                queue.append((neighbour, steps+1))
                visited.add(neighbour)

    if max_steps%2==0:
        return even_visited
    else:
        return odd_visited

def show(data_map, visited):
    ilen = len(data)
    jlen = len(data[0])
    print(ilen, jlen)
    i_order = list(map(lambda x: x[0], visited))
    j_order = list(map(lambda x: x[1], visited))
    imin, imax = min(i_order), max(i_order)
    jmin, jmax = min(j_order), max(j_order)
    for i in range(imin, imax+1):
        line = ''
        for j in range(jmin, jmax+1):
            if (i,j) in visited:
                line += 'O'
            else:
                line += data_map[(i % ilen, j % jlen)]
        print(line)

with open('input.txt') as f:
    data = [[c for c in line.strip()] for line in f]
    data_map = {(i,j):data[i][j] for i in range(len(data)) for j in range(len(data[i]))}
    start = ()
    for node, value in data_map.items():
        if value == "S":
            start = node

    visited = bfs(start, data_map, 64)
    
    steps = 26501365
    # 26501365 % 131 = 65 a massive simplification!!
    # so the diamond ball goes all the way to the tip of the last repeat block
    # and there is no edge nonsense 
    xs = [65 + 131*n for n in range(4)]
    ys = [len(bfs(start, data_map, x)) for x in xs]
    z = np.polyfit(xs, ys, 2) # its a quadratic because area scales as r^2
    p = np.poly1d(z)
    # I hate this solutions but I'm not spending a single second more on it
    #show(data_map, visited)
    print(f"Part 1: {len(visited)}")
    print(f"Part 2: {int(p(steps))}") # and we round down?? no idea...
