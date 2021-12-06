from __future__ import annotations
import argparse
import logging
import sys
from collections import defaultdict
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


def load_input(fp: TextIO) -> list[int]:
    return [int(x) for x in fp.read().strip().split(',')]


def tick(stages: dict[int, int]) -> dict[int, int]:
    result = {
        0: stages[1],
        1: stages[2],
        2: stages[3],
        3: stages[4],
        4: stages[5],
        5: stages[6],
        6: stages[0] + stages[7],
        7: stages[8],
        8: stages[0]
    }
    return result


def puzzle1(data) -> int:
    stages: dict[int, int] = {}
    for i in range(9):
        stages[i] = 0
    for stage in data:
        stages[stage] += 1
    for i in range(80):
        logging.debug("On day %d there are %d fish.", i, sum(stages.values()))
        stages = tick(stages)
    return sum(stages.values())


def puzzle2(data) -> int:
    stages: dict[int, int] = {}
    for i in range(9):
        stages[i] = 0
    for stage in data:
        stages[stage] += 1
    for i in range(256):
        logging.debug("On day %d there are %d fish.", i, sum(stages.values()))
        stages = tick(stages)
    return sum(stages.values())


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
