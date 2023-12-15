from collections import defaultdict

def hasher(s):
    hash = 0
    for c in s:
        hash += ord(c)
        hash *= 17
        hash %= 256
    return hash
    
def total_hash(data):
    return sum([hasher(s) for s in data])

def get_boxes(data):
    # dictionaries in python preserve insertion order so can use for this
    boxes = defaultdict(lambda: defaultdict(int))
    for s in data:
        if '-' in s:
            label, _ = s.split('-')
            box = hasher(label)
            if label in boxes[box]:
                boxes[box].pop(label) 
        elif '=' in s:
            label, focal_l = s.split('=')
            box = hasher(label)
            boxes[box][label] = focal_l
    return boxes

def sum_boxes(boxes):
    total = 0
    for n, lenses in boxes.items():
        for i, (_,f) in enumerate(lenses.items()):
            total += (n+1)*(i+1)*int(f)
    return total
    
with open('input.txt') as f:
    data = []
    for l in f:
        l = l.strip()
        data = l.split(',')

    print(f"Part 1: {total_hash(data)}")

    boxes = get_boxes(data)
    print(f"Part 2: {sum_boxes(boxes)}")
