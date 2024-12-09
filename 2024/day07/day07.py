from __future__ import annotations
import argparse
import itertools
import logging
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


def load_input(fp: TextIO):
    data = []
    for line in fp:
        test_value, rest = line.strip().split(': ')
        data.append((int(test_value), [int(n) for n in rest.split()]))
    return data


def is_valid1(total: int, numbers: list[int]) -> bool:
    operators = list(itertools.product('*+', repeat=len(numbers) - 1))
    for op_set in operators:
        answer = numbers[0]
        i = 1
        for op in op_set:
            answer = eval(f"{answer} {op} {numbers[i]}")
            i += 1
        if answer == total:
            return True
    return False


def puzzle1(data: list[tuple[int, list[int]]]) -> int:
    total = 0
    for entry in data:
        if is_valid1(entry[0], entry[1]):
            # print(entry)
            total += entry[0]
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
