import re

# part 1
with open('input.txt') as f:
    total = 0
    for line in f.readlines():
        line = line.strip()
        nums = []
        for c in line:
            if c.isnumeric():
                nums.append(int(c))
        total += nums[0]*10 + nums[-1]
    print(f"Part 1: {total}")

# part 2
with open('input.txt') as f:
    total = 0
    numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    for line in f.readlines():
        line = line.strip()
        nums = []
        for i, c in enumerate(line):
            if c.isnumeric():
                nums.append((int(c), i))
        for n, number in enumerate(numbers):
            num_indices = [m.start() for m in re.finditer(number, line)]
            for num_idx in num_indices:
                nums.append((n+1,num_idx))
        nums = sorted(nums, key=lambda x: x[1])
        if len(nums) > 0:
            total += 10*nums[0][0] + nums[-1][0]
    print(f"Part 2: {total}")
