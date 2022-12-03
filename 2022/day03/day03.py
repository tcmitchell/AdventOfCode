from __future__ import annotations
import argparse
import logging
import string
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
    return [line.strip() for line in fp.readlines()]


def split_load(load: str) -> tuple[str, str]:
    """Split the load into the two compartments."""
    size = len(load) // 2
    return load[:size], load[size:]


def duplicate_item(ruck: tuple[str, str]) -> str:
    """Find the one duplicate item in the two compartments."""
    set1 = set(ruck[0])
    set2 = set(ruck[1])
    items = set1.intersection(set2)
    assert len(items) == 1
    return items.pop()


SCORE_TABLE = list(string.ascii_letters)


def item_priority(item: str) -> int:
    return SCORE_TABLE.index(item) + 1


def puzzle1(data: list[str]) -> int:
    rucks = [split_load(load) for load in data]
    dups = [duplicate_item(ruck) for ruck in rucks]
    return sum([item_priority(item) for item in dups])


def common_item(groups: list[str]) -> str:
    set_groups = [set(g) for g in groups]
    return set_groups[0].intersection(set_groups[1]).intersection(set_groups[2]).pop()


def puzzle2(data: list[str]) -> int:
    # split data into groups of 3 elves
    # Locate the common item in each group
    badges = []
    for i in range(0, len(data), 3):
        badges.append(common_item(data[i:i+3]))
    return sum([item_priority(item) for item in badges])


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
