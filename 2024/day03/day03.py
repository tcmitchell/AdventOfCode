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


def load_input(fp: TextIO):
    return fp.read()

MUL_RE= re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

def puzzle1(data) -> int:
    mul_statements = MUL_RE.findall(data)
    total = 0
    for mul_statement in mul_statements:
        x = int(mul_statement[0])
        y = int(mul_statement[1])
        # print(f'{x} * {y}')
        total += x * y
    return total

MULDO_RE= re.compile(r'(mul\((\d{1,3}),(\d{1,3})\))|(do\(\))|(don\'t\(\))')

def puzzle2(data) -> int:
    statements = MULDO_RE.findall(data)
    enabled = True
    total = 0
    for statement in statements:
        # print(statement)
        if statement[0] and enabled:
            total += int(statement[1]) * int(statement[2])
        elif statement[3]:
            enabled = True
        elif statement[4]:
            enabled = False
    return total


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
