from __future__ import annotations
import argparse
import copy
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


def is_cycle(data: list[list[str]], pos: tuple[int, int]) -> bool:
    data[pos[0]][pos[1]] = '#'
    r, c = find_guard(data)
    visited = {(r, c, data[r][c])}
    while guard_in_room(data, (r, c)):
        r, c = move_and_mark(data, (r, c))
        try:
            guard = data[r][c]
        except IndexError:
            return False
        assert(guard in {'^', '>', 'v', '<'})
        if (r, c, guard) in visited:
            print("loop detected")
            return True
        visited.add((r, c, guard))
    return False


def puzzle2A(data: list[list[str]]) -> int:
    logger = logging.getLogger('puzzle2')
    save_data = copy.deepcopy(data)
    guard_pos = find_guard(data)
    initial_pos = guard_pos
    t = 0
    while guard_in_room(data, guard_pos):
        guard_pos = move_and_mark(data, guard_pos)
        t += 1
    show_room(data, logger)
    candidates = []
    for r in range(len(data)):
        for c in range(len(data[r])):
            if data[r][c] == 'X' and (r, c) != initial_pos:
                candidates.append((r, c))
    logger.info("There are %d candidates", len(candidates))
    cycles = 0
    checked = 0
    for candidate in candidates:
        data = copy.deepcopy(save_data)
        if is_cycle(data, candidate):
            cycles += 1
        checked += 1
        if checked % 10 == 0:
            logger.info("Checked %d candidates, have %d cycles", checked, cycles)
    return cycles


def find_looped_route(start_pos, next_row, next_col, grid):
    row_count = len(grid)
    col_count = len(grid[0])
    curr_row, curr_col = start_pos
    visited = set()

    while True:
        # Add coords to visited
        visited.add((curr_row, curr_col, next_row, next_col))
        # Bounds check (is guard gonna leave)
        if curr_row + next_row < 0 or curr_row + next_row >= row_count or curr_col + next_col < 0 or curr_col + next_col >= col_count:
            break
        # Check for obstacle else move
        if grid[curr_row + next_row][curr_col + next_col] == "#":
            next_col, next_row = -next_row, next_col
        else:
            curr_row += next_row
            curr_col += next_col
        # Check if looped
        if (curr_row, curr_col, next_row, next_col) in visited:
            return True


# Thanks to https://github.com/IchBinJade/advent-of-code-python/blob/main/2024%2Fday06.py
def puzzle2(grid: list[list[str]]) -> int:
    start_pos = find_guard(grid)
    total = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] != ".":
                continue
            grid[row][col] = "#"
            if find_looped_route(start_pos, -1, 0, grid):
                total += 1
            grid[row][col] = "."
    return total


# puzzle 2: 1713 is too high

def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(copy.deepcopy(data))
    logging.info('Puzzle 1: %r', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %r', answer)


if __name__ == '__main__':
    main()
