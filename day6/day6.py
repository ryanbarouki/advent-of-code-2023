import math 
from functools import reduce

def solve_quadratic(a,b,c):
    if b**2 - 4*a*c < 0:
        raise Exception('No real solutions!')
    A = -b/(2*a)
    B = math.sqrt(b**2 - 4*a*c)/(2*a)
    return A-B, A+B

def find_min_max(time, dist):
    max, min = solve_quadratic(-1, time, -dist)
    round_min = math.ceil(min)
    round_max = math.floor(max)
    if round_min == min:
        round_min += 1
    if round_max == max:
        round_max -= 1
    return round_max - round_min + 1

def part_1(times_records):
    prod = 1
    for T, dist in times_records:
        prod *= find_min_max(T, dist)
    return prod

with open('input.txt') as f:
    times = []
    records = []
    for line in f.readlines():
        if 'Time' in line:
            _, time = line.split(':')
            times = [int(t) for t in time.split()]
        elif 'Distance' in line:
            _, distance = line.split(':')
            records = [int(x) for x in distance.split()]

    times_records = zip(times, records)
    
    # part 2
    time = int(reduce(lambda a,b: a+b, [str(t) for t in times]))
    record = int(reduce(lambda a,b: a+b, [str(x) for x in records]))
    
    print(f"Part 1: {part_1(times_records)}")
    print(f"Part 2: {find_min_max(time, record)}")

