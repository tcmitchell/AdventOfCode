from __future__ import annotations
import argparse
import logging
import math
import sys
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
    return [int(x) for x in fp.read().split(',')]


def cost1(start: int, end: int) -> int:
    return abs(end - start)


def puzzle1(data) -> int:
    logging.debug("Data = %r", data)
    min_cost = math.inf
    min_pos = min(data)
    max_pos = max(data)
    for p in range(min(data), max(data) + 1):
        cost = sum([cost1(loc, p) for loc in data])
        if cost < min_cost:
            min_cost = cost
            logging.debug("Position %d is cheaper at %d", p, cost)
    return min_cost


def cost2(start: int, end: int) -> int:
    n = abs(end - start)
    return (n * n + n)//2


def puzzle2(data) -> int:
    logging.debug("Data = %r", data)
    min_cost = math.inf
    min_pos = min(data)
    max_pos = max(data)
    for p in range(min(data), max(data) + 1):
        cost = sum([cost2(loc, p) for loc in data])
        if cost < min_cost:
            min_cost = cost
            logging.debug("Position %d is cheaper at %d", p, cost)
    return min_cost


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
