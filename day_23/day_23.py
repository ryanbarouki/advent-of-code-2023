from queue import PriorityQueue
from collections import deque, defaultdict
from copy import deepcopy, copy

def get_neighbours(node, data_map, can_climb):
    i,j = node
    neighbours = []
    if not can_climb:
        if data_map[node] in ['>','<','v']:
            match data_map[node]:
                case '>':
                    return [(i,j+1)]
                case '<':
                    return [(i,j-1)]
                case 'v':
                    return [(i+1,j)]
    for di,dj in [(0,1),(1,0),(0,-1),(-1,0)]:
        next = (i+di, j+dj)
        if next in data_map and data_map[next] != '#':
            neighbours.append(next)
    return neighbours

def make_adj_map(data_map, can_climb=False):
    adj_map = defaultdict(list)
    for node in data_map:
        if data_map[node] != '#':
            for k, neighbour in enumerate(get_neighbours(node, data_map, can_climb)):
                # node and distance to
                adj_map[node].append((neighbour, 1))
    return adj_map
            
def dfs(adj_map, start, end):
    queue = deque()
    visited = set()
    queue.append((start, 0, {start}))
    visited.add(start)
    paths = []
    distances = []

    while len(queue):
        node, dist, path = queue.pop()

        if node == end:
            distances.append(dist)
            continue

        for neighbour, dist_to in adj_map[node]:
            if neighbour not in path:
                queue.append((neighbour, dist+dist_to, path | {neighbour}))
    return max(distances)

def find_nearest_juncs(adj_map, start, junctions):
    queue = deque()
    visited = set()
    queue.append((start, 0))
    visited.add(start)

    nearest_juncs = set()
    while len(queue):
        node, dist = queue.popleft()

        if node in (junctions - {start}):
            nearest_juncs.add((node, dist))
            visited.add(node)
            continue

        neighbours = adj_map[node]
        for neighbour, d in neighbours:
            if neighbour not in visited:
                queue.append((neighbour, dist+1))
                visited.add(neighbour)
    return nearest_juncs

def get_junctions(adj_map):
    junctions = set()
    for node, neighbours in adj_map.items():
        if len(neighbours) > 2:
            junctions.add(node)
    return junctions

def compress_map(adj_map, junctions):
    new_map = defaultdict(set)
    for junc in junctions:
        new_map[junc] = find_nearest_juncs(adj_map, junc, junctions) 
    return new_map

def show(data, junctions):
    for i, row in enumerate(data):
        line = ''
        for j, c in enumerate(row):
            if (i,j) in junctions:
                line += 'O'
            else: 
                line += c
        print(line)

with open('input.txt') as f:
    data = [[c for c in line.strip()] for line in f]
    data_map = {(i,j):data[i][j] for i in range(len(data)) for j in range(len(data[i]))}
    start = (0,1)
    end = (len(data)-1, len(data[0])-2)
    adj1 = make_adj_map(data_map)
    print(f"Part 1: {dfs(adj1, start, end)}")

    adj2 = make_adj_map(data_map, can_climb=True)
    junctions = get_junctions(adj2) | {start, end}
    compressed_adj_map = compress_map(adj2, junctions)
    print(f"Part 2: {dfs(compressed_adj_map, start, end)}")
    #show(data,junctions)

