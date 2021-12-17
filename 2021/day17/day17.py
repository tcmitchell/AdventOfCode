from __future__ import annotations
import argparse
import logging
import re
from typing import TextIO


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType('r'),
                        metavar="PUZZLE_INPUT")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args(args)
    return args


def init_logging(debug=False):
    msg_format = '%(asctime)s %(levelname)s %(message)s'
    date_format = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msg_format, datefmt=date_format, level=level)


def load_input(fp: TextIO) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r'-?\d+', fp.read())))
    # return fp.read()


def step_probe(vx, vy, px, py) -> tuple[int, ...]:
    px += vx
    py += vy
    if vx > 0:
        vx -= 1
    elif vx < 0:
        vx += 1
    vy -= 1
    return vx, vy, px, py


def fire_probe(vx, vy, tx0, tx1, ty0, ty1) -> tuple[bool, int, int]:
    px = py = 0
    max_y = py
    max_x = px
    while px < tx1 and py > ty0:
        vx, vy, px, py = step_probe(vx, vy, px, py)
        max_x = max(max_x, px)
        max_y = max(max_y, py)
        # logging.debug("Probe: at %r with velocity %r", (px, py), (vx, vy))
        if tx0 <= px <= tx1 and ty0 <= py <= ty1:
            # In target zone
            # logging.debug("%r is in the target zone", (px, py))
            return True, max_x, max_y
    return False, max_x, max_y


def triangle(n) -> int:
    # Like factorial, only addition
    # See https://math.stackexchange.com/questions/593318/factorial-but-with-addition/593323
    return n * (n + 1) // 2


def puzzle1_orig(data: tuple[int, ...]) -> int:
    """This was my original fumbling around with the problem.
    It turns out you don't need most of it. You must need to compute
    the appropriate Y for launch, and the triangle number of that Y
    gives you the max altitude.
    """
    x0, x1, y0, y1 = data

    # X becomes zero at some point, so these are the possible X values
    # that land inside the target zone horizontally.
    x_values = []
    x = 0
    while True:
        tx = triangle(x)
        if tx > x1:
            break
        if x0 <= tx <= x1:
            x_values.append(x)
        x += 1

    # Y velocity decreases by 1, so it will always return to the
    # origin. From there, it must land inside the target zone, so it
    # must have a velocity when it crosses the origin such that
    # increasing by one more will hit the bottom of the target zone.
    y_value = abs(y0) - 1
    predicted_y = triangle(y_value)
    logging.debug("Predicted Y: %d", predicted_y)
    # Now figure out the max y height reached. There is probably a
    # formula here, like `triangle` above, and X probably doesn't
    # matter.
    real_max_y = 0
    for x in x_values:
        in_zone, _, max_y = fire_probe(x, y_value, x0, x1, y0, y1)
        if in_zone and max_y > real_max_y:
            real_max_y = max_y

    # in_zone, max_y = fire_probe(7, 2, x0, x1, y0, y1)
    # in_zone, max_y = fire_probe(6, 3, x0, x1, y0, y1)
    # in_zone, max_x, max_y = fire_probe(17, -4, x0, x1, y0, y1)
    # in_zone, max_x, max_y = fire_probe(7, 9, x0, x1, y0, y1)
    return real_max_y


def puzzle1(data: tuple[int, ...]) -> int:
    x0, x1, y0, y1 = data
    # Y velocity decreases by 1, so it will always return to the
    # origin. From there, it must land inside the target zone, so it
    # must have a velocity when it crosses the origin such that
    # increasing by one more will hit the bottom of the target zone.
    y_value = abs(y0) - 1
    max_y = triangle(y_value)
    return max_y


def show_all():
    all_text = """23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7"""
    all_pairs = list(map(int, re.findall(r'-?\d+', all_text)))
    pairs = [(all_pairs[i], all_pairs[i+1]) for i in range(0, len(all_pairs), 2)]
    pairs.sort()
    for pair in pairs:
        print(pair)


def puzzle2(data) -> int:
    # show_all()
    x0, x1, y0, y1 = data

    # X becomes zero at some point, so these are the possible X values
    # that land inside the target zone horizontally.
    x_values = []
    x = 0
    while True:
        tx = triangle(x)
        if tx > x1:
            break
        if x0 <= tx <= x1:
            x_values.append(x)
        x += 1
    min_x = min(x_values)
    max_x = max(x0, x1)
    # Y velocity decreases by 1, so it will always return to the
    # origin. From there, it must land inside the target zone, so it
    # must have a velocity when it crosses the origin such that
    # increasing by one more will hit the bottom of the target zone.
    max_y = abs(y0) - 1

    velocities = []
    for x in range(min_x, max_x + 1):
        # logging.debug("Exploring x = %d", x)
        for y in range(y0, max_y + 1):
            in_zone, _, _ = fire_probe(x, y, x0, x1, y0, y1)
            if in_zone:
                velocities.append((x, y))
    return len(velocities)


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(data)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main()
