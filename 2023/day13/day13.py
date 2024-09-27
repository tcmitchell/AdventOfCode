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
    all_data = fp.read()
    data = all_data.split('\n\n')
    maps = [map.split() for map in data]
    return maps


def check_symmetry(grid, row1, row2):
    nrows = min(row1 + 1, # account for the 0th row
                len(grid) - row2)
    logging.info("checking symmetry of %d rows", nrows)
    for i in range(nrows):
        if grid[row1 - i] != grid[row2 + i]:
            return False
    return True


def find_symmetry(grid):
    for i in range(len(grid) - 1):
        if grid[i] == grid[i + 1]:
            logging.info("Possible symmetry at %d, %d", i, i + 1)
            if check_symmetry(grid, i, i + 1):
                return i + 1
    return None


def transpose(grid: list[str]) -> list[str]:
    tmap = []
    for i in range(len(grid[0])):
        tmap.append([])
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            tmap[x].append(grid[y][x])
    tgrid = [''.join(x) for x in tmap]
    return tgrid


def puzzle1(maps: list[list[str]]) -> int:
    vsum = 0
    hsum = 0
    for i, grid in enumerate(maps):
        tgrid = transpose(grid)
        logging.info("Examining grid %d for vertical symmetry", i)
        result = find_symmetry(tgrid)
        if result is not None:
            vsum += result
            continue
        logging.info("Examining grid %d for horizontal symmetry", i)
        result = find_symmetry(grid)
        if result is not None:
            hsum += result
            continue
    return vsum + (100 * hsum)


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
