from math import lcm

def find_path_length(instructions, move_map, start='AAA', stop_func=lambda x: x == 'ZZZ'):
    i = 0
    current = start
    lr_to_01 = {'L': 0, 'R': 1}
    instructions = list(map(lambda x: lr_to_01[x], instructions))
    count = 0
    while not stop_func(current):
        current = move_map[current][instructions[i]]
        i += 1
        i %= len(instructions)
        count += 1
    return count

def part_2(instructions, move_map):
    # turns out the period of each one starts at the beginning and repeats
    # so we can just find the time it takes to get to the first 'Z' and 
    # find the LCM
    current_places = list(filter(lambda x: x[-1] == 'A', move_map))
    periods = []
    for current in current_places:
        periods.append(find_path_length(instructions, move_map, 
                              start=current, 
                              stop_func=lambda x: x[-1] == 'Z'))
    return lcm(*periods)

with open('input.txt') as f:
    instructions = []
    move_map = {}
    for i, line in enumerate(f.readlines()):
        line = line.strip()
        if i == 0:
            instructions = line
        elif len(line) > 0:
            key, value = line.split('=')
            value = value.strip()
            left, right = value[1:-1].split(',')
            move_map[key.strip()] = (left.strip(), right.strip())

    print(f"Part 1: {find_path_length(instructions, move_map)}")
    print(f"Part 2: {part_2(instructions, move_map)}")
            

