from copy import deepcopy

class Brick:
    def __init__(self, cubes):
        self.cubes = cubes
        zs = map(lambda x: x[2], cubes)
        self.min_z = min(zs)

    def __repr__(self):
        return f"cubes={self.cubes}, min_z={self.min_z}"

def create_brick(start, end):
    x1,y1,z1 = start
    x2,y2,z2 = end
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    brick = set()
    if dx == dy == dz == 0:
        brick.add((x1,y1,z1))
    elif dx != 0:
        for x in range(x1,x2+1):
            brick.add((x,y1,z1))
    elif dy != 0:
        for y in range(y1,y2+1):
            brick.add((x1,y,z1))
    elif dz != 0:
        for z in range(z1,z2+1):
            brick.add((x1,y1,z))
    return Brick(brick)

def brick_is_floating(brick, settled):
    for cube in brick.cubes:
        x,y,z = cube
        if (x,y,z-1) in settled or z == 1:
            settled |= brick.cubes
            return False
    return True

def lower_brick(brick):
    lower = set()
    for cube in brick.cubes:
        x,y,z = cube
        lower.add((x,y,z-1))
    return Brick(lower)

def settle_bricks(bricks):
    sort_bricks = sorted(bricks, key=lambda x: x.min_z)
    settled_bricks = []
    settled = set()
    for brick in sort_bricks:
        if brick.min_z == 1:
            settled |= brick.cubes
            settled_bricks.append(brick)
            continue
        while brick_is_floating(brick, settled):
            brick = lower_brick(brick)
        settled_bricks.append(brick)
    return settled_bricks

def get_cubes(bricks):
    cubes = set()
    for b in bricks:
        cubes |= b.cubes
    return cubes
         

def can_disintegrate(i, bricks):
    bricks_copy = deepcopy(bricks)
    bricks_copy.pop(i)
    settled = settle_bricks(bricks_copy)
    if get_cubes(settled) == get_cubes(bricks_copy):
        return True
    return False



with open('input.txt') as f:
    bricks = []
    for line in f:
        start, end = line.strip().split('~')
        x1,y1,z1 = start.split(',')
        x2,y2,z2 = end.split(',')
        start = (int(x1),int(y1),int(z1))
        end = (int(x2),int(y2),int(z2))
        bricks.append(create_brick(start, end))

    settled = settle_bricks(bricks)
    count = 0
    for i in range(len(settled)):
        if can_disintegrate(i, settled):
            print(count)
            count += 1
    print(count)
