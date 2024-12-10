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
    data = []
    for line in fp:
        data.append([int(x) for x in list(line.strip())])
    return data


def find_path(grid, r, c, height) -> list[tuple[int, int]]:
    if (r, c) not in grid:
        # we've gone off the grid
        return []
    if grid[(r, c)] != height + 1:
        # not a gentle rise
        return []
    if grid[(r, c)] == 9:
        # we've reached a summit
        logging.info("Summit at (%d, %d)", r, c)
        return [(r, c)]
    result = list()
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        result.extend(find_path(grid, r + dr, c + dc, height + 1))
    return result


def puzzle1(data) -> int:
    grid = {}
    for r in range(len(data)):
        for c in range(len(data[r])):
            grid[(r, c)] = data[r][c]
    total = 0
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c] == 0:
                summits = set(find_path(grid, r, c, -1))
                logging.info("Summits for (%d, %d): %r", r, c, summits)
                total += len(summits)
    return total


def puzzle2(data) -> int:
    grid = {}
    for r in range(len(data)):
        for c in range(len(data[r])):
            grid[(r, c)] = data[r][c]
    total = 0
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c] == 0:
                trails = find_path(grid, r, c, -1)
                logging.info("Trails for (%d, %d): %r", r, c, trails)
                total += len(trails)
    return total


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
