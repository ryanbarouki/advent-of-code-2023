from collections import deque
from functools import cache

@cache
def dp(seq, groups):
    # base cases
    if not seq:
        # no more sequence left so add 1 if groups are also done, else 0
        return groups == ()
    if not groups:
        # no more groups so return 1 if the rest of seq is '.', else 0
        return '#' not in seq

    # recursive time (one day dynamic programming will be natural I hope)
    # also what even is DP?? - someone explain pls
    count = 0
    if seq[0] in ['.','?']:
        # we go again if c = . or ?
        count += dp(seq[1:],groups) 
    if seq[0] in ['#','?']:
        ns, ng = len(seq), groups[0]
        # is the length of remaining sequence enough to fit the group?
        # if we have a '.' in the section up to group length then it's not
        # gonna work so do nothing
        if ns >= ng and '.' not in seq[:ng]:
            # if the remaining sequence length == group length 
            # => continue recursion
            # or if the next character in the sequence after the end of
            # the group is a '.' or a '?'. A '#' would extend the group so we 
            # recursing in that case.
            if ng == ns or seq[ng] != '#':
                # continue skipping the group in the seq
                # and pop it from groups
                count += dp(seq[ng+1:], groups[1:])
    return count

with open('input.txt') as f:
    total_part1 = 0
    total_part2 = 0
    for line in f.readlines():
        s, counts = line.strip().split()
        counts = tuple([int(n) for n in counts.split(',')])
        count1 = dp(s, counts)
        total_part1 += count1

        # part 2
        s_part2 = "?".join([s for i in range(5)])
        counts_part2 = 5*counts
        count2 = dp(s_part2, counts_part2)
        total_part2 += count2

    print(f"Part 1: {total_part1}")
    print(f"Part 2: {total_part2}")

