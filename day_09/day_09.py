def predict_next(numbers):
    differences = [numbers]
    curr_difference = numbers
    while not all(n == 0 for n in curr_difference):
        next_diffs = []
        for i, n in enumerate(curr_difference):
            if i < len(curr_difference)-1:
                next_diffs.append(curr_difference[i+1] - n)
        differences.append([*next_diffs])
        curr_difference = [*next_diffs]

    differences.reverse()

    for j, diffs in enumerate(differences):
        if j == 0:
            diffs.append(0)
            continue
        diffs.append(differences[j-1][-1] + diffs[-1])
    
    return differences[-1][-1]

def add_predicted(lines, reverse=False):
    total = 0
    for numbers in lines:
        if reverse:
            reversed = [*numbers]
            reversed.reverse()
            numbers = reversed
        total += predict_next(numbers) 
    return total 

with open('input.txt') as f:
    lines = []
    for line in f.readlines():
        lines.append([int(n) for n in line.split()])

    print(f"Part 1: {add_predicted(lines)}")
    print(f"Part 2: {add_predicted(lines, reverse=True)}")
