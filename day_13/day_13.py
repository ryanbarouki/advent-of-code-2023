import numpy as np
from copy import deepcopy

def is_mirror(b, i, check_range):
    for j in range(check_range):
        if b[i-1-j] != b[i+2+j]:
            return False
    return True

def count_rows(b):
    counts = set()
    count = 0
    for i, row in enumerate(b):
        if i == len(b) - 1:
            break
        next = b[i+1]
        if row == next:
            check_range = min(i, len(b)-i-2)
            if check_range == 0:
                count = i+1
                counts.add(count)
                count = 0
            elif is_mirror(b, i, check_range):
                count += i + 1
                counts.add(count)
                count = 0
    return counts if counts else set([0])

def remove_smudge(b):
    count = 0
    flip = {'#':'.', '.':'#'}
    for i, row in enumerate(b):
        for j, c in enumerate(row):
            new_b = deepcopy(b)
            new_b[i][j] = flip[c]
            changed, new, is_horizontal = has_changed(b, new_b)
            if changed:
                return 100*new if is_horizontal else new

def has_changed(b1, b2):
    # Don't really like this function but too tired to care
    b1_h = count_rows(b1)
    b2_h = count_rows(b2) - b1_h
    b2_h = b2_h.pop() if b2_h else 0
    b1_h = b1_h.pop() 

    b1t = np.array([[c for c in line] for line in b1]).T
    b1t = [[c for c in line] for line in b1t]
    b2t = np.array([[c for c in line] for line in b2]).T
    b2t = [[c for c in line] for line in b2t]

    b1_v = count_rows(b1t)
    b2_v = count_rows(b2t) - b1_v
    b2_v = b2_v.pop() if b2_v else 0
    b1_v = b1_v.pop()


    if b2_h == 0 and b2_v == 0:
        # no lines of reflection
        return False, 0, None

    if b1_h != 0 and b2_h != 0 and b1_h != b2_h:
        # is a horizontal to new horizontal
        return True, b2_h, True
    if b1_h == 0 and b2_h != 0:
        # vertical to horizontal
        return True, b2_h, True

    if b1_v != 0 and b2_v != 0 and b1_v != b2_v:
        # is a vertical to new vertical
        return True, b2_v, False
    if b1_v == 0 and b2_v !=0:
        # horizontal to vertical
        return True, b2_v, False
    return False, 0, None

with open('input.txt') as f:
    blocks = []
    block = []
    blocks_t = []
    for line in f.readlines():
        line = line.strip()
        if len(line) != 0:
            block.append([c for c in line])
        else: 
            blocks.append(block)
            block_t = np.array([[c for c in line] for line in block]).T
            block_t = [[c for c in line] for line in block_t]
            blocks_t.append(block_t)
            block = []

    print("Part 1")
    print(100*sum([count_rows(b).pop() for b in blocks]) + sum([count_rows(b).pop() for b in blocks_t]))
    print("Part 2")
    print(sum([remove_smudge(b) for b in blocks]))
    

