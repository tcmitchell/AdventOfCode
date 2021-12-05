from __future__ import annotations
import argparse
import logging
import sys
from collections import defaultdict
from typing import TextIO

def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType('r'),
                        metavar="PUZZLE_INPUT")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    return args


def init_logging(debug=False):
    msgFormat = '%(asctime)s %(levelname)s %(message)s'
    dateFormat = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msgFormat, datefmt=dateFormat, level=level)


def load_input(fp: TextIO):
    data = [line.strip().split('->') for line in fp.readlines()]
    result = []
    for row in data:
        row_data = []
        for pair in row:
            coords = pair.strip().split(',')
            row_data.append([int(c) for c in coords])
        result.append(row_data)
    return result


def fill_horizontal(grid: defaultdict, x1, x2, y):
    if x1 > x2:
        x2, x1 = x1, x2
    x = x1
    while x <= x2:
        grid[(x, y)] += 1
        x += 1


def fill_vertical(grid: defaultdict, x, y1, y2):
    if y1 > y2:
        y2, y1 = y1, y2
    y = y1
    while y <= y2:
        grid[(x, y)] += 1
        y += 1


def fill_diagonal(grid: defaultdict, x1, y1, x2, y2):
    logging.debug("Diagonal: (%d, %d) -> (%d, %d)", x1, y1, x2, y2)
    x_step = 1
    if x1 > x2:
        x_step = -1
    x_coords = range(x1, x2 + x_step, x_step)
    y_step = 1
    if y1 > y2:
        y_step = -1
    y_coords = range(y1, y2 + y_step, y_step)
    for i in range(len(x_coords)):
        grid[(x_coords[i], y_coords[i])] += 1


def print_grid(grid, max_x, max_y):
    print('-' * max_x * 2)
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in grid:
                print(grid[(x, y)], end='')
            else:
                print('.', end='')
        print()
    print('-' * max_x * 2)
    print()


def puzzle1(data) -> int:
    grid = defaultdict(int)
    for duct in data:
        x1 = duct[0][0]
        y1 = duct[0][1]
        x2 = duct[1][0]
        y2 = duct[1][1]
        if x1 == x2:
            fill_vertical(grid, x1, y1, y2)
        elif y1 == y2:
            fill_horizontal(grid, x1, x2, y1)
        else:
            logging.debug('Skipping %r', duct)
    # print_grid(grid, 10, 10)
    return len([count for count in grid.values() if count > 1])


def puzzle2(data) -> int:
    grid = defaultdict(int)
    for duct in data:
        x1 = duct[0][0]
        y1 = duct[0][1]
        x2 = duct[1][0]
        y2 = duct[1][1]
        if x1 == x2:
            fill_vertical(grid, x1, y1, y2)
        elif y1 == y2:
            fill_horizontal(grid, x1, x2, y1)
        else:
            fill_diagonal(grid, x1, y1, x2, y2)
    # print_grid(grid, 10, 10)
    return len([count for count in grid.values() if count > 1])


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
