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


ALL_NUMBERS_RE = re.compile(r"[\-\d]+")


def load_input(fp: TextIO):
    result = []
    for l in fp:
        numbers = ALL_NUMBERS_RE.findall(l)
        logging.debug("numbers: %r", numbers)
        result.append([int(x) for x in numbers])
    return result


def compute_differences(seq: list[int]) -> list[int]:
    result = []
    for i in range(len(seq) - 1):
        result.append(seq[i+1] - seq[i])
    return result

def all_zeros(seq: list[int]) -> bool:
    return all((n == 0 for n in seq))


def puzzle1(data) -> int:
    total = 0
    for seq in data:
        s = seq
        stack = []
        while not all_zeros(s):
            stack.append(s[-1])
            s = compute_differences(s)
        logging.debug("Stack: %r", stack)
        # Now add
        a = 0
        while stack:
            a += stack.pop(0)
        total += a
        logging.debug("Next number: %r", a)

    return total


def puzzle2(data) -> int:
    return 0


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
