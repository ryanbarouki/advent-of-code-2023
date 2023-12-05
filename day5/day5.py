class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Interval({self.start}, {self.end})"

    def __and__(self, other):
        new_start = max(self.start, other.start)
        new_end = min(self.end, other.end)
        if new_start <= new_end:
            return Interval(new_start, new_end)
        return None  # empty

def map_value(value, map):
    for ranges in map:
        destination, source, length = ranges
        if value >= source and value <= source + length:
            return destination + (value - source)
    return value

def map_interval(X, map):
    intersecting_intervals = []
    non_intersecting_intervals = []

    current_start = X.start

    final_mapped = []
    # Sort intervals based on start number
    for ranges in sorted(map, key=lambda x: x[1]):
        destination, source, length = ranges
        interval = Interval(source, source + length)
        intersection = X & interval
        if intersection:
            if current_start < intersection.start:
                non_intersecting_intervals.append(Interval(current_start, intersection.start))
            intersecting_intervals.append(intersection)
            final_mapped.append(Interval(destination + intersection.start - source, destination + intersection.end - source))
            current_start = intersection.end

    # Check for any remaining non-intersecting part of X
    if current_start < X.end:
        non_intersecting_intervals.append(Interval(current_start, X.end))
    return sorted([*final_mapped, *non_intersecting_intervals], key=lambda x: x.start)


def part1(seeds, maps):
    values = []
    for seed in seeds:
        value = seed
        for i, map in enumerate(maps):
            value = map_value(value, map)
        values.append(value)
    return min(values)

def part2(seed_data, maps):
    seed_ranges = []
    for i in range(0,len(seed_data),2):
        seed_ranges.append(Interval(seed_data[i], seed_data[i] + seed_data[i+1]))
    location_intervals = []
    for seed_interval in seed_ranges:
        intervals_to_map = [seed_interval]
        for map in maps:
            next_intervals = []
            for interval in intervals_to_map:
                next_intervals = [*next_intervals, *map_interval(interval, map)]
            intervals_to_map = [*next_intervals]
        location_intervals = [*location_intervals, *intervals_to_map]

    sorted_locations = sorted(location_intervals, key=lambda x: x.start)
    return sorted_locations[0].start


with open('input.txt') as f:
    seeds = []
    maps = []

    current_map = []
    for line in f.readlines():
        if 'seeds' in line:
            _, seeds = line.split(':')
            seeds = [int(seed) for seed in seeds.split()]
        elif 'map' not in line:
            ranges = [int(num) for num in line.split()]
            if len(ranges) > 0:
                current_map.append(ranges)
        else:
            maps.append(current_map)
            current_map = []
    maps.append(current_map) #last one

    maps = maps[1:] # jank
    print(f"Part 1: {part1(seeds, maps)}")
    print(f"Part 2: {part2(seeds, maps)}")
