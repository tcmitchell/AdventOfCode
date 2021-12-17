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
        logging.debug("Probe: at %r with velocity %r", (px, py), (vx, vy))
        if tx0 <= px <= tx1 and ty0 <= py <= ty1:
            # In target zone
            logging.debug("%r is in the target zone", (px, py))
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


def puzzle2(data) -> int:
    return 0


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
