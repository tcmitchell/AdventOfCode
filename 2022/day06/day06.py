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


def load_input(fp: TextIO) -> str:
    return fp.read()


def all_different(data: str) -> bool:
    chars = list(data)
    while chars:
        item = chars.pop()
        if item in chars:
            return False
    return True


def puzzle1(data: str) -> int:
    for idx in range(len(data) - 4):
        if all_different(data[idx:idx+4]):
            return idx + 4
    return 0


def puzzle2(data) -> int:
    for idx in range(len(data) - 14):
        if all_different(data[idx:idx+14]):
            return idx + 14
    return 0


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(data)
    # answer = puzzle1('mjqjpqmgbljsphdztnvjfqwrcgsmlb')
    # answer = puzzle1('bvwbjplbgvbhsrlpgdmjqwftvncz')
    # answer = puzzle1('nppdvjthqldpwncqszvftbrmjlhg')
    # answer = puzzle1('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg')
    # answer = puzzle1('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw')
    logging.info('Puzzle 1: %r', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %r', answer)


if __name__ == '__main__':
    main()
