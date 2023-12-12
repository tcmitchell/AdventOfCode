from __future__ import annotations
import argparse
import functools
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


@functools.cache
def num_valid_arrangements(springs: str, clues: tuple[int, ...], run_size: int = 0) -> int:
    # Thank you https://www.reddit.com/r/adventofcode/comments/18ghle1/2023_day_12_part_2_python_i_love_you_python/
    # print(springs, clues, run_size)
    if not springs:
        if ((len(clues) == 1 and clues[0] == run_size)
                or (len(clues) == 0 and run_size == 0)):
            return 1
        return 0
    spring = springs[0]
    springs = springs[1:]
    clue, *new_clues = clues or [0]
    new_clues = tuple(new_clues)
    if spring == '?':
        return (num_valid_arrangements('#'+springs, clues, run_size) +
                num_valid_arrangements('.'+springs, clues, run_size))
    elif spring == '#':
        if run_size > clue:
            return 0
        return num_valid_arrangements(springs, clues, run_size + 1)
    elif spring == '.':
        if run_size != 0 and run_size != clue:
            return 0
        return num_valid_arrangements(springs, new_clues if run_size else clues, 0)
    else:
        raise ValueError("Spring not one of #.?")


def unfold(seq: str, score: tuple[int, ...]) -> tuple[str, tuple[int, ...]]:
    return '?'.join([seq] * 5), score * 5


def puzzle2(data) -> int:
    total_ways = 0
    for seq, score in data:
        useq, uscore = unfold(seq, score)
        ways = num_valid_arrangements(useq, uscore)
        logging.debug("%s %r  - %d arrangements", seq, score, ways)
        total_ways += ways
    return total_ways


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
