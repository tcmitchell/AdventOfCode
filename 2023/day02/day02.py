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


def load_input(fp: TextIO):
    return [line.strip() for line in fp]


GAME_ID_RE = re.compile(r"Game (\d+):")

def parse_id(line: str) -> int:
    match = GAME_ID_RE.match(line)
    if match is None:
        raise ValueError(f"Malformed game: {line}")
    return int(match.group(1))

RED_CUBES_RE = re.compile(r"(\d+) red")
GREEN_CUBES_RE = re.compile(r"(\d+) green")
BLUE_CUBES_RE = re.compile(r"(\d+) blue")

def parse_cubes_max(line: str) -> tuple[int, int, int]:
    games = line.split(':')[1]
    # print(games)
    red = max([int(x) for x in (RED_CUBES_RE.findall(games))])
    green = max([int(x) for x in (GREEN_CUBES_RE.findall(games))])
    blue = max([int(x) for x in (BLUE_CUBES_RE.findall(games))])
    return red, green, blue

def puzzle1(data) -> int:
    possible = 0
    for game in data:
        # extract game id
        game_id = parse_id(game)
        # print(game_id)
        r, g, b = parse_cubes_max(game)
        if r > 12 or g > 13 or b > 14:
            continue
        possible += game_id
    return possible


def puzzle2(data) -> int:
    total_power = 0
    for game in data:
        r, g, b = parse_cubes_max(game)
        power = r * g * b
        total_power += power
    return total_power


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
