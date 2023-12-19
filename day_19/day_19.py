from collections import deque

def lambda_factory(condition):
    x = condition[0]
    return eval(f"lambda {x}: {condition}")

def sum_parts(parts):
    total = 0
    for part in parts:
        for _, value in part.items():
            total += value
    return total

def is_accepted(part, workflows):
    curr_workflow = 'in'
    decided = False
    while True:
        for (check_cat, check, outcome) in workflows[curr_workflow]:
            cat = part[check_cat] if check_cat else 0
            if check(cat):
                if outcome == 'R':
                    return False
                elif outcome == 'A':
                    return True
                else:
                    curr_workflow = outcome 
                    break

def process(parts, workflows):
    accepted_list = []
    for part in parts:
        if is_accepted(part, workflows):
            accepted_list.append(part)
    return accepted_list

def get_prod(part):
    subtot = 1
    for _, ranges in part.items():
        low, hi = ranges
        subtot *= (hi-low)+1
    return subtot

def find_combinations(workflows):
    combinations = 0
    curr_workflow = 'in'
    queue = deque()
    queue.append(({'x':(1,4000),'m':(1,4000),'a':(1,4000),'s':(1,4000)}, workflows[curr_workflow]))
    while len(queue):
        node, workflow = queue.popleft()
        cat, condition, outcome = workflow.popleft()

        if not cat:
            # last condition
            if outcome == 'A':
                combinations += get_prod(node)
            elif outcome == 'R':
                pass
            else:
                new = {key:val for key,val in node.items()}
                queue.append((new, workflows[outcome]))
            continue

        # not last condition
        comparitor, value = condition[0], int(condition[1:])

        # sort the ranges out first
        lower, upper = node[cat]
        if comparitor == '<':
            range1, range2 = (lower, value-1), (value, upper)
        elif comparitor == '>':
            range1, range2 = (lower, value), (value+1, upper)

        new1 = {key:val for key,val in node.items()}
        new2 = {key:val for key,val in node.items()}
        new1[cat] = range1
        new2[cat] = range2
        if outcome == 'A':
            if comparitor == '<':
                # add product of values lower range
                combinations += get_prod(new1)
                # add upper range to queue with remaining workflow
                queue.append((new2, workflow))
            elif comparitor == '>':
                # add product of values upper range
                combinations += get_prod(new2)
                # add lower range to queue with remaining workflow
                queue.append((new1, workflow))
        elif outcome == 'R':
            if comparitor == '<':
                # add upper range to queue with remaining workflow
                new1[cat] = range2
            elif comparitor == '>':
                # add lower range to queue with remaining workflow
                new1[cat] = range1
            queue.append((new1, workflow))
        else:
            # outcome points to new workflow
            if comparitor == '<':
                # lower range will go to new workflow
                queue.append((new1, workflows[outcome]))
                # upper range will stay on this workflow but next one 
                queue.append((new2, workflow))
            if comparitor == '>':
                # upper range will go to new workflow
                queue.append((new2, workflows[outcome]))
                # lower range will stay on this workflow but next one
                queue.append((new1, workflow))
    return combinations

with open('input.txt') as f:
    parts = []
    workflows = {}
    workflows2 = {}
    for line in f:
        line = line.strip()
        if line and line[0] != "{":
            name, rest = line.split('{')
            checks = rest.split(',')
            first_checks = checks[:-1]
            last_outcome = checks[-1][:-1]
            check_list = []
            check_list2 = deque()
            for c in first_checks:
                condition, outcome = c.split(':')
                check_list.append((condition[0], lambda_factory(condition), outcome))
                check_list2.append((condition[0], condition[1:], outcome)) 
            check_list.append((None, lambda x: True, last_outcome))
            check_list2.append((None, None, last_outcome))
            workflows[name] = check_list
            workflows2[name] = check_list2

        elif line and line[0] == "{":
            vals = line.strip('{}').split(',')
            part_deets = {} 
            for val in vals:
                kind, num = val.split('=')
                part_deets[kind] = int(num)
            parts.append(part_deets)
    print(f"Part 1: {sum_parts(process(parts, workflows))}")
    print(f"Part 2: {find_combinations(workflows2)}") #126107942006821
