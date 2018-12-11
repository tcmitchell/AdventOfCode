import argparse
import collections
import datetime
import itertools
import logging
import re
import sys
import time

# Wrong: 235, 31
# Right: 235,31

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


def load_input(fp):
    return int(fp.read())


Point = collections.namedtuple('Point', ['x', 'y', 'vx', 'vy'])


def hundreds_digit(x):
    if x < 100:
        return 0
    else:
        return int(str(x)[-3])


def power_level(x, y, sn):
    rack_id = x + 10
    power = rack_id * y
    power += sn
    power *= rack_id
    power = hundreds_digit(power)
    return power - 5


def square_power(grid, x, y):
    return (grid[x][y] + grid[x + 1][y] + grid[x + 2][y]
            + grid[x][y + 1] + grid[x + 1][y + 1] + grid[x + 2][y + 1]
            + grid[x][y + 2] + grid[x + 1][y + 2] + grid[x + 2][y + 2])


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    serial_number = load_input(args.input)
    logging.info('serial number: {}'.format(serial_number))
    
    grid = [[None] * 300 for x in range(300)]
    for x in range(300):
        for y in range(300):
            grid[x][y] = power_level(x + 1, y + 1, serial_number)

    max_power = -1
    max_power_origin = (0, 0)
    for x in range(298):
        for y in range(298):
            sp = square_power(grid, x, y)
            if sp > max_power:
                max_power = sp
                max_power_origin = (x + 1, y + 1)

    logging.info('max_power: {} at {}'.format(max_power, max_power_origin))
    print('Answer: {}, {}'.format(max_power_origin[0], max_power_origin[1]))

    for y in range(42, 49):
        for x in range(30, 37):
            print(grid[x][y], end=' ')
        print()

    print()
    print('{}, {}, {}'.format(grid[32][44], grid[33][44], grid[34][44]))
    print('{}, {}, {}'.format(grid[32][45], grid[33][45], grid[34][45]))
    print('{}, {}, {}'.format(grid[32][46], grid[33][46], grid[34][46]))
    print('sp: {}'.format(square_power(grid, 32, 44)))

if __name__ == '__main__':
    main(sys.argv)
