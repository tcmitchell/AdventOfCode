from __future__ import annotations
import argparse
import itertools
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


ALL_NUMBERS_RE = re.compile(r"\d+")
ALL_HASH_GROUPS_RE = re.compile(r"#+")


def load_input(fp: TextIO) -> list[tuple[str, tuple[int, ...]]]:
    result = []
    for line in fp:
        line = line.strip()
        row, raw_counts = line.split(' ')
        counts = (int(n) for n in ALL_NUMBERS_RE.findall(raw_counts))
        result.append((row, tuple(counts)))
    return result


def score_seq(seq: str) -> tuple[int, ...]:
    return tuple(len(g) for g in ALL_HASH_GROUPS_RE.findall(seq))


def evaluate_replacement(pattern: str, r: tuple[str, ...]) -> tuple[int, ...]:
    seq = pattern % r
    score = score_seq(seq)
    logging.debug("seq = %r; score %r", seq, score)
    return score


def count_ways(orig: str, score: tuple[int, ...]) -> int:
    ptrn = orig.replace('?', '%s')
    expected_hashes = sum(score)
    actual_hashes = orig.count('#')
    needed_hashes = expected_hashes - actual_hashes
    actual_wild = orig.count('?')
    replacements = '#' * (needed_hashes)
    replacements += '.' * (actual_wild - len(replacements))
    logging.debug("replacements: %s", replacements)
    ways = 0
    replacements = set(r for r in itertools.product(('#', '.'), repeat=actual_wild)
                       if r.count('#') == needed_hashes)
    for p in replacements:
        if evaluate_replacement(ptrn, p) == score:
            ways += 1
    return ways

def puzzle1(data) -> int:
    total_ways = 0
    for seq, score in data:
        total_ways += count_ways(seq, score)
    return total_ways


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
