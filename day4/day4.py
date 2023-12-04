
def part1(shared_nums):
    total = 0
    for shared in shared_nums:
        if len(shared) > 0:
            total += pow(2, len(shared) - 1)
    return total

def part2(multiplicities, number_of_winning):
    for game in number_of_winning:
        winning = number_of_winning[game]
        if winning > 0:
            for i in range(winning):
                multiplicities[game+i+1] += multiplicities[game]

    return sum([val for key,val in multiplicities.items()])


with open('input.txt') as f:
    shared_nums = []
    lines = f.readlines()
    # for part 2
    multiplicities = {}
    number_of_winning = {}
    for line in lines:
        line = line.strip()
        card, numbers = line.split(':')
        _, card_num = card.split()
        winning_numbers, my_numbers = numbers.split('|')
        winning_numbers = set([int(num) for num in winning_numbers.split()])
        my_numbers = set([int(num) for num in my_numbers.split()])
        shared = winning_numbers & my_numbers
        shared_nums.append(shared)

        # for part 2
        multiplicities[int(card_num)] = 1
        number_of_winning[int(card_num)] = len(shared)

    print(f"Part 1: {part1(shared_nums)}")
    print(f"Part 2: {part2(multiplicities, number_of_winning)}")

