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

NUMBER_RE = re.compile(r"\d+")

def load_input(fp: TextIO):
    return [[int(x) for x in NUMBER_RE.findall(line)]
            for line in fp]


def puzzle1(data) -> int:
    print(data)
    col1 = []
    col2 = []
    for a, b in data:
        col1.append(a)
        col2.append(b)
    col1.sort()
    col2.sort()
    total = 0
    for a, b in zip(col1, col2):
        print(a, b)
        total += abs(a - b)
    return total


def puzzle2(data) -> int:
    col1 = []
    col2 = []
    for a, b in data:
        col1.append(a)
        col2.append(b)
    similarity = 0
    for x in col1:
        similarity += col2.count(x) * x
    return similarity


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(data)
    logging.info('Puzzle 1: %r', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %r', answer)


if __name__ == '__main__':
    main()
