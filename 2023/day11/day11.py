from __future__ import annotations
import argparse
import logging
from itertools import combinations
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


def load_input(fp: TextIO) -> list[list[str]]:
    return [list(line.strip()) for line in fp]


def expand_rows(data: list[list[str]]) -> None:
    empty_rows = [i for i, r in enumerate(data) if '#' not in r]
    # Reverse so the rows don't shift out from underneath us
    for i in reversed(empty_rows):
        logging.debug("Expanding row %d", i)
        data.insert(i, data[i].copy())


def galaxy_in_column(data: list[list[str]], c: int) -> bool:
    for r in data:
        if r[c] == '#':
            return True
    return False


def insert_empty_column(data: list[list[str]], c: int) -> None:
    for row in data:
        row.insert(c, '.')


def expand_columns(data: list[list[str]]) -> None:
    empty_columns = []
    for c in range(len(data[0])):
        if not galaxy_in_column(data, c):
            empty_columns.append(c)
    for c in reversed(empty_columns):
        logging.debug("Expanding column %d", c)
        insert_empty_column(data, c)


def galaxy_locations(data: list[list[str]]) -> list[tuple[int, int]]:
    result = []
    for r, row in enumerate(data):
        row: list[str]
        for c in range(len(row)):
            if row[c] == '#':
                result.append((r, c))
    return result


def taxi_distance(g1: tuple[int, int], g2: tuple[int, int]) -> int:
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


def puzzle1(data: list[list[str]]) -> int:
    expand_rows(data)
    expand_columns(data)
    for row in data:
        logging.debug("".join(row))
    galaxies = galaxy_locations(data)
    for galaxy in galaxies:
        logging.debug("Galaxy %r", galaxy)
    total_distance = 0
    for pair in combinations(galaxies, 2):
        logging.debug("Pair %r", pair)
        total_distance += taxi_distance(pair[0], pair[1])
    return total_distance


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
