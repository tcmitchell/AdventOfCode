from __future__ import annotations
import argparse
import logging
import re
from typing import TextIO

# 625 is too high

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


INT_PATTERN = re.compile(r'\d+')


def load_input(fp: TextIO) -> list[list[int]]:
    parsed = (INT_PATTERN.findall(line) for line in fp.readlines())
    return [[int(x) for x in row] for row in parsed]


def puzzle1(data: list[list[int]]) -> int:
    tally = 0
    for s1, e1, s2, e2 in data:
        # print(f'{s1}-{e1},{s2}-{e2}')
        if s1 <= s2 and e1 >= e2:
            # elf 1 subsumes elf2
            tally += 1
        elif s2 <= s1 and e2 >= e1:
            # elf 2 subsumes elf 1
            tally += 1
    return tally


def puzzle2(data) -> int:
    tally = 0
    for s1, e1, s2, e2 in data:
        if e1 < s2 or e2 < s1:
            tally += 1
    return len(data) - tally


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
