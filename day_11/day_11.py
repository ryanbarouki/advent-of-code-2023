import numpy as np

def calculate_distances(galaxies, blank_rows, blank_cols, expansion=1):
    dist = 0
    for k, g1 in enumerate(galaxies):
        for l in range(k+1,len(galaxies)):
            i1, j1 = g1
            i2, j2 = galaxies[l]
            g1_to_g2 = abs(i2-i1) + abs(j2-j1)
            for row in blank_rows:
                if min(i1,i2) < row < max(i1,i2):
                    g1_to_g2 += expansion
            for col in blank_cols:
                if min(j1,j2) < col < max(j1,j2):
                    g1_to_g2 += expansion
            dist += g1_to_g2
    return dist


with open('input.txt') as f:
    galaxies = []
    blank_rows = set()
    blank_cols = set()
    universe = []
    for i, line in enumerate(f.readlines()):
        universe.append([c for c in line.strip()])
        if '#' not in line:
            blank_rows.add(i)
        for j, c in enumerate(line):
            if c == '#':
                galaxies.append((i,j))

    universe_np = np.array(universe)
    for j, line in enumerate(universe_np.T):
        if '#' not in line:
            blank_cols.add(j)

    print(f"Part 1: {calculate_distances(galaxies, blank_rows, blank_cols)}")
    print(f"Part 2: {calculate_distances(galaxies, blank_rows, blank_cols, expansion=1_000_000-1)}")

