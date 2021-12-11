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
    return [[int(x) for x in list(line.strip())] for line in fp.readlines()]


def neighbors(x, y):
    result = [(x-1, y-1), (x-1, y), (x-1, y+1),
              (x, y-1), (x, y+1),
              (x+1, y-1), (x+1, y), (x+1, y+1)]
    result = [(x, y) for x, y in result if 0 <= x < 10 and 0<= y < 10]
    return result


def step_energy(energy: list[list[int]]) -> int:
    # Return the number of flashes
    flashers = {}
    for y in range(10):
        for x in range(10):
            energy[y][x] += 1
            if energy[y][x] > 9:
                flashers[(x, y)] = False
    flashq = list(flashers.keys())
    while flashq:
        x, y = flashq.pop(0)
        if flashers[(x, y)]:
            logging.debug("%r already flashed", (x, y))
        # logging.debug("Flash %r", (x, y))
        flashers[(x, y)] = True
        for x, y in neighbors(x, y):
            energy[y][x] += 1
            if energy[y][x] > 9 and (x, y) not in flashers:
                flashers[(x, y)] = False
                flashq.append((x, y))
    for x, y in flashers.keys():
        energy[y][x] = 0
    return len(flashers)


def puzzle1(energy: list[list[int]]) -> int:
    flash_count = 0
    for step in range(100):
        logging.debug("----- Stepping Energy -----")
        flash_count += step_energy(energy)
        logging.debug("Flash count: %d", flash_count)
    return flash_count


def puzzle2(data) -> int:
    return 0


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(data)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main()
