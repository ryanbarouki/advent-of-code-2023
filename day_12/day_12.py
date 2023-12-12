def binary_strings(n, s=""):
    if n == 0:
        yield s
    else:
        yield from binary_strings(n-1,s+'#')
        yield from binary_strings(n-1,s+'.')

def find_runs(s,char):
    counts = []
    count = 1
    for i, c in enumerate(s):
        if i < len(s) - 1:
            next_c = s[i+1]
            if c != char:
                continue
            if c == next_c:
                count += 1
            else:
                counts.append(count)
                count = 1
        else:
            if c == char:
                counts.append(count)
    return tuple(counts)

with open('input.txt') as f:
    total = 0
    for line in f.readlines():
        s, counts = line.strip().split()
        counts = tuple([int(n) for n in counts.split(',')])

        count_qm = s.count('?')
        for bs in binary_strings(count_qm):
            new_s = ''
            index = 0
            for c in s:
                if c != '?':
                    new_s += c
                else:
                    new_s += bs[index]
                    index += 1
            curr_counts = find_runs(new_s, '#')
            if counts == curr_counts:
                total += 1
    print(total)
            


