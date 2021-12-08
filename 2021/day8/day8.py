from __future__ import annotations
import argparse
import logging
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


def load_input(fp: TextIO) -> list[list[str]]:
    result = []
    for line in fp:
        parts = line.split('|')
        parts = [p.strip() for p in parts]
        digits = [d.strip() for d in parts[1].split()]
        patterns = [p.strip() for p in parts[0].split()]
        result.append([patterns, digits])
    return result


def puzzle1(data) -> int:
    # Extract just the digits portion of the data
    digits = [d[1] for d in data]
    target = [2, 4, 3, 7]
    total = 0
    for entry in digits:
        total += sum([1 for item in entry if len(item) in target])
    return total


def puzzle2(data) -> int:
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
