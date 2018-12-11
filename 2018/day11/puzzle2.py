import argparse
import collections
import datetime
import itertools
import logging
import re
import sys
import time

# Right: 241,65,10

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


def square_power(grid, xo, yo, size):
    sp = 0
    for x in range(xo, xo + size):
        sp += sum(grid[x][yo:yo+size])
    return sp


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
    for size in range(300):
#    for size in [3]:
        logging.info('Size {}'.format(size))
        for x in range(301 - size):
            for y in range(301 - size):
                try:
                    sp = square_power(grid, x, y, size)
                    if sp > max_power:
                        max_power = sp
                        max_power_origin = (x + 1, y + 1)
                        logging.info('max_power: {} at {}'.format(max_power, max_power_origin))
                except IndexError:
                    continue

    logging.info('max_power: {} at {}'.format(max_power, max_power_origin))
    print('Answer: {}, {}'.format(max_power_origin[0], max_power_origin[1]))


if __name__ == '__main__':
    main(sys.argv)
