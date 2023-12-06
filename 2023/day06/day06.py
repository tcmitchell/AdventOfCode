from __future__ import annotations
import argparse
import logging
import math
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


ALL_INTS_RE = re.compile(r"\d+")


def load_input(fp: TextIO):
    times = [int(x) for x in ALL_INTS_RE.findall(fp.readline())]
    distances = [int(x) for x in ALL_INTS_RE.findall(fp.readline())]
    return list(zip(times, distances))


def simulate1(p: int, t: int):
    """Simulate how far a ship goes if button pressed for `p` millis."""
    result = p * (t - p)
    logging.debug("Holding button for %d millis goes %d mm in %d seconds", p, result, t)
    return p * (t - p)


def binary_search_leftmost(t: int, d: int) -> int:
    L = 0
    R = t
    while L < R:
        m = math.floor((L + R) / 2)
        if simulate1(m, t) < d + 1:
            L = m + 1
        else:
            R = m
    return L


def binary_search_rightmost(t: int, d: int) -> int:
    L = 0
    R = t
    while L < R:
        m = math.floor((L + R) / 2)
        if simulate1(m, t) < d + 1:
            R = m
        else:
            L = m + 1
    return R - 1

def puzzle1(data) -> int:
    all_counts = []
    for t, d in data:
        left = binary_search_leftmost(t, d)
        right = binary_search_rightmost(t, d)
        count = right - left + 1
        logging.debug("%d %d: left = %d; right = %d; count = %d", t, d, left, right, count)
        all_counts.append(count)
    return math.prod(all_counts)


def puzzle2(data) -> int:
    t = int("".join([str(x[0]) for x in data]))
    d = int("".join([str(x[1]) for x in data]))
    left = binary_search_leftmost(t, d)
    right = binary_search_rightmost(t, d)
    count = right - left + 1
    logging.debug("%d %d: left = %d; right = %d; count = %d", t, d, left, right, count)
    return count


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
