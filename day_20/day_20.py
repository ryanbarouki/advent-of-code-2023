from enum import Enum
from collections import defaultdict, deque
from math import lcm
from copy import deepcopy

class Pulse(Enum):
    HIGH = 1
    LOW = 2

class Module:
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs
    
    def receive_pulse(self, sender, pulse):
        return []

    def __repr__(self):
        return f"Name: {self.name}, Outputs: {self.outputs}"
    
class FlipFlop(Module):
    def __init__(self, name, outputs):
        self.on = False
        super().__init__(name, outputs)

    def receive_pulse(self, sender, pulse):
        # returns list of outputs to send pulse to and what kind (module, high/low)
        outs = []
        if pulse == Pulse.HIGH:
            # do nothin
            return []
        elif pulse == Pulse.LOW:
            to_send = Pulse.LOW if self.on else Pulse.HIGH
            self.on = not self.on
            for out in self.outputs:
                outs.append((self.name, out, to_send))
        return outs

class Conjunction(Module):
    def __init__(self, name, outputs):
        self.memory = defaultdict(lambda: Pulse.LOW)
        super().__init__(name, outputs)

    def receive_pulse(self, sender, pulse):
        outs = []
        self.memory[sender] = pulse
        to_send = Pulse.LOW if all(self.memory[x] == Pulse.HIGH for x in self.memory) else Pulse.HIGH
        for out in self.outputs:
            outs.append((self.name, out, to_send))
        return outs

    def initialise(self, sender):
        self.memory[sender] = Pulse.LOW

class Broadcaster(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)

    def receive_pulse(self, sender, pulse):
        outs = []
        for out in self.outputs:
            outs.append((self.name, out, pulse))
        return outs

def make_module(m_type, name, outputs):
    if m_type == '%':
        return FlipFlop(name, outputs)
    elif m_type == '&':
        return Conjunction(name, outputs)

def press_button(modules):
    hi_count = 0
    low_count = 0
    broadcaster = modules['broadcaster']
    first_modules = broadcaster.receive_pulse(None, Pulse.LOW)
    queue = deque()
    for module in first_modules:
        queue.append(module)
    while len(queue):
        sender, name, pulse = queue.popleft()
        if pulse == Pulse.LOW:
            low_count += 1
        else:
            hi_count += 1
        curr_module = modules[name] if name in modules else Module(name,[])
        next_modules = curr_module.receive_pulse(sender, pulse)
        for next in next_modules:
            queue.append(next)
    return hi_count, low_count

def press_and_check(modules, i, receiver, chosen_sender, chosen_pulse):
    broadcaster = modules['broadcaster']
    first_modules = broadcaster.receive_pulse(None, Pulse.LOW)
    queue = deque()
    for module in first_modules:
        queue.append(module)
    while len(queue):
        sender, name, pulse = queue.popleft()
        curr_module = modules[name] if name in modules else Module(name,[])
        if name == receiver and sender == chosen_sender and pulse == chosen_pulse:
            return i+1
        next_modules = curr_module.receive_pulse(sender, pulse)
        for next in next_modules:
            queue.append(next)
    return -1

def initialise(modules):
    for name, module in modules.items():
        for name2 in module.outputs:
            module2 = modules[name2] if name2 in modules else Module(name,[])
            if isinstance(module2, Conjunction):
                module2.initialise(name)
        
def part1(modules, num_presses):
    hi_count = 0
    low_count = 0
    initialise(modules)
    for _ in range(num_presses):
        hi, low = press_button(modules)
        hi_count += hi
        low_count += low+1
    return (hi_count)*(low_count)

def part2(modules, receiver, sender, pulse):
    i = 0
    initialise(modules)
    while True:
        count = press_and_check(modules, i, receiver, sender, pulse)
        if count != -1:
            return count
        i += 1

with open('input.txt') as f:
    modules = {}
    for line in f:
        module, outputs = line.strip().split('->')
        module = module.strip()
        outputs = outputs.strip().split(', ')
        if module == 'broadcaster':
            modules[module] = Broadcaster('broadcaster', outputs)
        else:
            m_type, m_name = module[0], module[1:]
            modules[m_name] = make_module(m_type, m_name, outputs)

    print(f"Part 1: {part1(deepcopy(modules), 1000)}")
    # Part 2
    # Bit jankkk
    # cl, rp, lb, nj -> lx -> rx
    # find when cl, rp, lb, nj sends a high pulse to lx and LCM it
    # cl = 3733
    # rp = 4091
    # lb = 3911
    # nj = 4093
    cl = part2(deepcopy(modules), 'lx', 'cl', Pulse.HIGH)
    rp = part2(deepcopy(modules), 'lx', 'rp', Pulse.HIGH)
    lb = part2(deepcopy(modules), 'lx', 'lb', Pulse.HIGH)
    nj = part2(deepcopy(modules), 'lx', 'nj', Pulse.HIGH)
    print(f"Part 2: {lcm(cl,rp,lb,nj)}")
