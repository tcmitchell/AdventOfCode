from __future__ import annotations
import argparse
import itertools
import logging
import re
from collections.abc import Sequence
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


def is_safe(report: Sequence[int]) -> bool:
    sorted_report = sorted(report)
    rev_sorted_report = sorted(report, reverse=True)
    if report != sorted_report and report != rev_sorted_report:
        return False
    for a, b in itertools.pairwise(report):
        delta = abs(a - b)
        if delta not in (1, 2, 3):
            return False
    return True


def puzzle1(data) -> int:
    safe = []
    for report in data:
        if is_safe(report):
            safe.append(report)
    return len(safe)


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
