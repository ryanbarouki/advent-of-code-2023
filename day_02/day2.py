def parse(lines):
    games = []
    for line in lines:
        line = line.strip()
        game, rest = line.split(':')
        rounds = rest.strip().split(';')
        round_list = []
        for round in rounds:
            cubes = round.split(',')
            cube_dict = {}
            for cube in cubes:
                num, colour = cube.strip().split(' ')
                cube_dict[colour] = int(num)
            round_list.append(cube_dict)
        games.append(round_list)
    return games

def part1(games):
    MAX_VALS = {'red': 12, 'green': 13, 'blue': 14}
    total = 0
    for i, game in enumerate(games):
        is_valid = True
        for round in game:
            for colour in round:
                is_valid = is_valid and round[colour] <= MAX_VALS[colour]
        if is_valid:
            total += i + 1
    return total

def part2(games):
    total = 0
    for game in games:
        min_vals = {}
        power = 1
        for colour in ['red', 'green', 'blue']:
            power *= max(list(map(lambda round: round[colour] if colour in round else 0, game)))
        total += power
    return total

with open('input.txt') as f:
    games = parse(f.readlines())
    print(f"Part 1: {part1(games)}")
    print(f"Part 2: {part2(games)}")



    

