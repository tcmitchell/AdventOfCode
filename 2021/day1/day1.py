import argparse
import collections
import logging
import re
import sys
import time

# Time step 10459, message = NEXPLRXK


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
    return [int(x) for x in fp]


def puzzle1(depths):
    increases = 0
    current = depths[0]
    for d in depths[1:]:
        if d > current:
            increases += 1
        current = d
    return increases


def puzzle2(depths):
    tri_depths = [sum(depths[i:i+3]) for i in range(len(depths) - 2)]
    return puzzle1(tri_depths)


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    depths = load_input(args.input)
    logging.debug('Loaded %d depths', len(depths))
    increases = puzzle1(depths)
    logging.info('Puzzle 1: %d', increases)
    increases = puzzle2(depths)
    logging.info('Puzzle 2: %d', increases)


if __name__ == '__main__':
    main(sys.argv)
