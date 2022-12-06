from __future__ import annotations
import argparse
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


INT_PATTERN = re.compile(r'\d+')


def build_towers(tower_defs: list[str]):
    # ' 1   2   3   4   5   6   7   8   9 '
    towers = []
    for i in range(9):
        towers.append([])
    indices = [1, 5, 9, 13, 17, 21, 25, 29, 33]
    tower_defs.reverse()
    for line in tower_defs:
        if '[' not in line:
            continue
        for i, idx in enumerate(indices):
            if line[idx].strip():
                towers[i].append(line[idx])
    return towers


def load_input(fp: TextIO):
    lines = fp.readlines()
    # Divide lines
    towers = []
    commands = []
    for line in lines:
        if not line.strip():
            continue
        if line.startswith('move'):
            commands.append([int(x) for x in INT_PATTERN.findall(line)])
        else:
            towers.append(line)
    towers2 = build_towers(towers)
    return towers2, commands


def puzzle1(towers: list[list[str]], commands: list[list[int]]) -> str:
    for count, origin, dest in commands:
        for i in range(count):
            towers[dest-1].append(towers[origin-1].pop())
    return ''.join([tower[-1] for tower in towers])


def puzzle2(towers: list[list[str]], commands: list[list[int]]) -> str:
    for count, origin, dest in commands:
        towers[dest-1].extend(towers[origin-1][-count:])
        towers[origin-1] = towers[origin-1][:-count]
    return ''.join([tower[-1] for tower in towers])


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    towers, commands = load_input(args.input)
    answer = puzzle1(towers, commands)
    logging.info('Puzzle 1: %r', answer)
    with open('input.txt') as input_fp:
        towers, commands = load_input(input_fp)
    answer = puzzle2(towers, commands)
    logging.info('Puzzle 2: %r', answer)


if __name__ == '__main__':
    main()
