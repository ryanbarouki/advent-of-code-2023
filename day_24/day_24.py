from math import sqrt

def find_intersection_2d(h0, h1):
    p0, v0 = h0
    p1, v1 = h1
    x0,y0,_ = p0
    x1,y1,_ = p1
    vx0,vy0,_ = v0
    vx1,vy1,_ = v1
    m0 = vy0/vx0
    m1 = vy1/vx1

    if m0 == m1:
        # parallel so no intersection
        return

    x_int = (y1 - y0 + m0*x0 - m1*x1)/(m0-m1)
    y_int = y0 + m0*(x_int - x0)
    return (x_int, y_int)

def normalise_2d(p):
    x,y,z = p
    norm = sqrt(x**2 + y**2)
    return (round(x/norm, 5), round(y/norm, 5))

def in_future(p, v, p_int):
    x,y,z = p 
    x_int, y_int = p_int
    diff = (x_int - x, y_int - y,  0)
    diff_norm = normalise_2d(diff) 
    v_norm = normalise_2d(v)
    return diff_norm == v_norm

def part1(data):
    lower, upper = 200_000_000_000_000, 400_000_000_000_000
    #lower, upper = 7,27
    count_ints = 0
    for i, h0 in enumerate(data):
        p0, v0 = h0
        for j in range(i, len(data)):
            h1 = data[j]
            p1, v1 = h1
            intersection = find_intersection_2d(h0, h1)
            if intersection:
                x_int, y_int = intersection
                if lower <= x_int <= upper and lower <= y_int <= upper:
                    if in_future(p0, v0, intersection) and in_future(p1, v1, intersection):
                        count_ints += 1
    return count_ints

def part2(data):
    # From Mathematica lol
    # Solved 6 equations for 6 unknowns by finding a line that intersects
    # 3 of the given lines
    # x -> 187016878804004, y -> 175507140888229, z -> 177831791810924
    # u -> 210, v -> 192, w -> 179
    p = (187016878804004,175507140888229,177831791810924)
    vel = (210,192,179)
    x,y,z = p
    vx,vy,vz = vel
    times = []
    for pi, vi in data:
        xi, _, _ = pi
        vxi, _, _ = vi
        ti = (xi-x)/(vx-vxi)
        times.append((ti, pi, vi))
    t0, p0, v0 = sorted(times, key=lambda x: x[0]).pop()
    x0,y0,z0 = p0
    vx0,vy0,vz0 = v0
    s = (x-x0+vx*t0)/vx0
    return (x+vx*(t0-s),y+vy*(t0-s),z+vz*(t0-s))



with open('input.txt') as f:
    data = []
    for line in f:
        pos, vel = line.strip().split('@')
        pos = pos.strip().split(', ')
        vel = vel.strip().split(', ')
        pos = tuple([int(n) for n in pos])
        vel = tuple([int(n) for n in vel])
        data.append((pos,vel))

    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {int(sum(part2(data)))}")

