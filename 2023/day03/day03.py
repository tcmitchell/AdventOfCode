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
    return [line.strip() for line in fp]


PART_NUMBER_RE = re.compile(r"\d+")
SYMBOL_RE = re.compile(r"[^\d.]")


def symbol_adjacent(schematic: list[str], row: int, start: int, end: int) -> bool:
    max_pos = len(schematic[0])
    # Check the row above
    if row > 0 and SYMBOL_RE.search(schematic[row-1], max(0, start-1), min(max_pos, end+1)) is not None:
        return True
    # Check left
    if start > 0 and SYMBOL_RE.search(schematic[row], start-1, start) is not None:
        return True
    # Check right
    if end < max_pos and SYMBOL_RE.search(schematic[row], end, end+1) is not None:
        return True
    # Check below
    if row + 1 < len(schematic) and SYMBOL_RE.search(schematic[row+1],
                                                     max(0, start-1),
                                                     min(max_pos, end+1)) is not None:
        return True
    return False


def puzzle1(data) -> int:
    sum_part_numbers = 0
    for row, line in enumerate(data):
        match = PART_NUMBER_RE.search(line)
        while match is not None:
            logging.debug("row %d: part %s at %d", row, match.group(0), match.start())
            if symbol_adjacent(data, row, match.start(), match.end()):
                sum_part_numbers += int(match.group(0))
            match = PART_NUMBER_RE.search(line, match.end())
    return sum_part_numbers


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
