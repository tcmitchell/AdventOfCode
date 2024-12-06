from __future__ import annotations
import argparse
import logging
from typing import TextIO, Optional


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
    return [list(line.strip()) for line in fp]


def find_guard(data: list[list[str]]) -> tuple[int, int]:
    for r in range(len(data)):
        try:
            c = data[r].index('^')
            return r, c
        except ValueError:
            pass
    raise ValueError("No guard found")


def is_blocked(data: list[list[str]], pos: tuple[int, int]) -> bool:
    r, c = pos
    try:
        return data[r][c] == '#'
    except IndexError:
        return False

def move_and_mark(data: list[list[str]], pos: tuple[int, int]) -> tuple[int, int]:
    """Move the guard and mark the previous position."""
    r, c = pos
    new_guard = data[r][c]
    dr = dc = 0
    match data[r][c]:
        case '^':
            dr = -1
            if is_blocked(data, (r + dr, c + dc)):
                new_guard = '>'
                dr = 0
                dc = 1
        case 'v':
            dr = 1
            if is_blocked(data, (r + dr, c + dc)):
                new_guard = '<'
                dr = 0
                dc = -1
        case '<':
            dc = -1
            if is_blocked(data, (r + dr, c + dc)):
                new_guard = '^'
                dr = -1
                dc = 0
        case '>':
            dc = 1
            if is_blocked(data, (r + dr, c + dc)):
                new_guard = 'v'
                dr = 1
                dc = 0
        case _:
            raise ValueError(f"No guard found: '{data[r][c]}'")
    # Now update the map
    data[r][c] = 'X'
    try:
        data[r + dr][c + dc] = new_guard
    except IndexError:
        # The guard has left the room. Don't worry about setting the new_guard position
        pass
    return r + dr, c + dc


def guard_in_room(data: list[list[str]], pos: tuple[int, int]) -> bool:
    r, c = pos
    return 0 <= r < len(data) and 0 <= c < len(data[0])


def show_room(data: list[list[str]], logger: Optional[logging.Logger] = None) -> None:
    if logger is None:
        logger = logging.getLogger('puzzle1')
    for row in data:
        logger.debug("%r", row)


def puzzle1(data: list[list[str]]) -> int:
    logger = logging.getLogger('puzzle1')
    show_room(data, logger)
    guard_pos = find_guard(data)
    logger.debug("Guard found: %r", guard_pos)
    t = 0
    while guard_in_room(data, guard_pos):
        guard_pos = move_and_mark(data, guard_pos)
        t += 1
        logger.debug("---------- time %d ----------", t)
        show_room(data, logger)
    visited = 0
    for row in data:
        visited += row.count('X')
    return visited


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
