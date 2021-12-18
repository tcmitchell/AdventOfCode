from __future__ import annotations
import argparse
import itertools
import logging
from copy import deepcopy
from typing import TextIO

from node import Pair, Node


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


def load_input(fp: TextIO) -> list[Node]:
    return [Pair.parse(snum.strip()) for snum in fp.readlines()]


def puzzle1(data: list[Node]) -> int:
    start = data.pop(0)
    while data:
        start = start.add(data.pop(0))
    logging.debug("After Add: %s", start)
    return start.magnitude()


def puzzle2(data: list[Node]) -> int:
    all_pairs = list(itertools.permutations(data, 2))
    max_magnitude = 0
    for pair in all_pairs:
        p1 = deepcopy(pair[0])
        p2 = deepcopy(pair[1])
        mag = p1.add(p2).magnitude()
        if mag > max_magnitude:
            logging.debug("New max: %d", mag)
            max_magnitude = mag
    return max_magnitude


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    data2 = deepcopy(data)
    answer = puzzle1(data)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(data2)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main()
