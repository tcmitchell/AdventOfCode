from __future__ import annotations
import argparse
import itertools
import logging
from collections import defaultdict
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
    data = []
    for line in fp:
        data.append(line.strip())
    return data


def compute_antinodes(a1: tuple[int, int], a2: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    dr = a1[0] - a2[0]
    dc = a1[1] - a2[1]
    return (a1[0] - 2 * dr, a1[1] - 2 * dc), (a2[0] + 2 * dr, a2[1] + 2 * dc)


def puzzle1(data) -> int:
    logger = logging.getLogger('puzzle1')
    grid = {}
    antennas = defaultdict(list)

    for r in range(len(data)):
        for c in range(len(data[0])):
            grid[(r, c)] = []
            if data[r][c] != '.':
                antennas[data[r][c]].append((r, c))
    antinodes = {}
    for k, v in antennas.items():
        logger.info("%s: %r", k, list(itertools.combinations(v, 2)))
        for a1, a2 in itertools.combinations(v, 2):
            logger.info("antennas: %r, %r", a1, a2)
            for antinode in compute_antinodes(a1, a2):
                logger.info("antinode: %r", antinode)
                if antinode in grid:
                    antinodes[antinode] = 1
    return len(antinodes)


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
