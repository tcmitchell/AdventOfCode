from __future__ import annotations
import argparse
import logging
import sys
from typing import TextIO, Tuple


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType('r'),
                        metavar="PUZZLE_INPUT")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    return args


def init_logging(debug=False):
    msg_format = '%(asctime)s %(levelname)s %(message)s'
    date_format = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msg_format, datefmt=date_format, level=level)


def load_input(fp: TextIO):
    lines = [list(line.strip()) for line in fp]
    result = []
    for line in lines:
        result.append([int(x) for x in line])
    return result


class Point:

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


def neighbors(depths: list[list[int]], x: int, y: int) -> list[Tuple[int, int]]:
    """Generate the list of neighboring points for the given point"""
    max_x = len(depths[0])
    max_y = len(depths)
    result = []
    for _x, _y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        if 0 <= _x < max_x and 0 <= _y < max_y:
            result.append((_x, _y))
    return result


def is_minima(depths: list[list[int]], x: int, y: int) -> bool:
    depth = depths[y][x]
    for neighbor in neighbors(depths, x, y):
        logging.debug("Point %d, %d has neighbor %r", x, y, neighbor)
        n_x = neighbor[0]
        n_y = neighbor[1]
        if depths[n_y][n_x] <= depth:
            return False
    return True


# 1797 is too high
def puzzle1(data: list[list[int]]) -> int:
    minima: list[Point] = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            if is_minima(data, x, y):
                minima.append(Point(x, y, data[y][x]))
    return sum([p.z + 1 for p in minima])


def puzzle2(data: list[list[int]]) -> int:
    return 0


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(data)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main(sys.argv)
