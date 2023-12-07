from functools import cmp_to_key

def cmp(item1, item2):
    priority = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    hand1, counts1, _ = item1
    hand2, counts2, _ = item2
    for i in range(min(len(counts1), len(counts2))):
        c1 = counts1[i]
        c2 = counts2[i]
        if c1 < c2:
            return -1
        elif c1 > c2:
            return 1

    # secondary compare
    for i, c1 in enumerate(hand1):
        c2 = hand2[i]
        p1 = priority[c1]
        p2 = priority[c2]
        if p1 < p2:
            return -1
        if p1 > p2: 
            return 1
    return 0

def cmp_part_2(item1, item2):
    priority = {'J': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                '9': 9, 'T': 10, 'Q': 12, 'K': 13, 'A': 14}
    hand1, _, _ = item1
    hand2, _, _ = item2
    type1 = determine_effective_type(hand1)
    type2 = determine_effective_type(hand2)
    if type1 < type2:
        return -1
    if type1 > type2:
        return 1

    # draw on value: check each card from start
    for i, c1 in enumerate(hand1):
        c2 = hand2[i]
        p1 = priority[c1]
        p2 = priority[c2]
        if p1 < p2:
            return -1
        if p1 > p2: 
            return 1
    return 0

def determine_effective_type(hand):
    counts_to_type = {(5,):7, (4,1):6, (3,2):5, (3,1,1):4, (2,2,1):3, (2,1,1,1):2, (1,1,1,1,1):1}
    count_non_jacks = []
    count_jacks = 0
    for c in set(hand):
        if c == 'J':
            count_jacks = hand.count(c)
        else:
            count_non_jacks.append(hand.count(c))
    count_non_jacks = sorted(count_non_jacks, reverse=True)

    if len(count_non_jacks) > 0:
        count_non_jacks[0] += count_jacks
    else:
        count_non_jacks = [5]

    return counts_to_type[tuple(count_non_jacks)]
    
            
def calculate_total(lines, cmp):
    ranked = sorted(lines, key=cmp_to_key(cmp))
    total = 0
    for i, item in enumerate(ranked):
        _, _, bid = item
        total += (i+1)*bid

    return total


with open('input.txt') as f:
    lines = []
    for line in f.readlines():
        hand, bid = line.split()
        counts = []
        for card in set(hand):
            counts.append(hand.count(card))
        counts = sorted(counts, reverse=True)
        lines.append((hand, counts, int(bid)))

    print(f"Part 1: {calculate_total(lines, cmp)}")
    print(f"Part 2: {calculate_total(lines, cmp_part_2)}")
          
