from __future__ import annotations
import argparse
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
    return [x.strip() for x in fp.readlines()]


def puzzle1(data) -> tuple[int, list[int]]:
    loads = []
    items = []
    for line in data:
        if not line:
            loads.append(sum(items))
            items = []
            continue
        items.append(int(line))
    return max(loads), loads


def puzzle2(loads: list[int]) -> int:
    loads.sort(reverse=True)
    return sum(loads[:3])


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer, loads = puzzle1(data)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(loads)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main()
