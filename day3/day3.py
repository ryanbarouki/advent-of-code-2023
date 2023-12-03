import re


def part1(lines):
    nums_idx = [[match.span() for match in re.finditer(r'\d+', line)] for line in lines]
    numbers = [[int(line[match.start():match.end()]) for match in re.finditer(r'\d+', line)] for line in lines]
    total = 0
    for i, row in enumerate(nums_idx):
        for k, (start, end) in enumerate(row):
            check_positions = []
            # prev row
            if i > 0:
                # above the number
                for j in range(start, end):
                    check_positions.append((i-1,j))
                # corners of previous row
                if start > 0:
                    check_positions.append((i-1,start-1))
                if end < len(lines[i]) - 1:
                    check_positions.append((i-1,end))
            # next row
            if i < len(nums_idx) - 1:
                # below the number
                for j in range(start, end):
                    check_positions.append((i+1,j))
                # corners of next row
                if start > 0:
                    check_positions.append((i+1,start-1))
                if end < len(lines[i]) - 1:
                    check_positions.append((i+1,end))
            # left and right of number
            if start > 0:
                # left
                check_positions.append((i, start-1))
            if end < len(lines[i]) - 1:
                # right
                check_positions.append((i, end))

            for l, col in check_positions:
                if re.fullmatch(r'[^.\d]', lines[l][col]) is not None:
                    total += numbers[i][k]
                    break
    return total



        

if __name__ == "__main__":
    with open('input.txt') as f:
        lines = [line.strip() for line in f.readlines()]
        print(f"Part 1: {part1(lines)}")


