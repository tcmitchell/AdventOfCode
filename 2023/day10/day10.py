from __future__ import annotations
import argparse
import logging
import typing
from enum import Enum
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


def load_input(fp: TextIO) -> list[str]:
    return [line.strip() for line in fp]


Map: typing.TypeAlias = list[str]


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


class Position(typing.NamedTuple):
    r: int
    c: int
    direction: typing.Optional[Direction] = None

    def find_neighbors(self, sketch: Map) -> list[Position]:
        result = []
        # NORTH
        if self.r - 1 >= 0:
            result.append(Position(self.r - 1, self.c, Direction.NORTH))
        # EAST
        if self.c + 1 < len(sketch[0]):
            result.append(Position(self.r, self.c + 1, Direction.EAST))
        # SOUTH
        if self.r + 1 < len(sketch):
            result.append(Position(self.r + 1, self.c, Direction.SOUTH))
        # WEST
        if self.c - 1 >= 0:
            result.append(Position(self.r, self.c - 1, Direction.WEST))
        return result


def find_start(sketch: list[str]) -> Position:
    for r, row in enumerate(sketch):
        if (c := row.find("S")) != -1:
            return Position(r, c)
    raise ValueError("No start found")


def find_start_position(sketch: Map, pos: Position) -> Position:
    # The starting position has two options for starting to navigate the path.
    for neighbor in pos.find_neighbors(sketch):
        logging.debug("Neighbor: %r", neighbor)
        match neighbor.direction:
            case Direction.NORTH:
                if sketch[neighbor.r][neighbor.c] in ['|', '7', 'F']:
                    return Position(pos.r, pos.c, neighbor.direction)
            case Direction.EAST:
                if sketch[neighbor.r][neighbor.c] in ['-', 'J', '7']:
                    return Position(pos.r, pos.c, neighbor.direction)
            case Direction.SOUTH:
                if sketch[neighbor.r][neighbor.c] in ['|', 'J', 'L']:
                    return Position(pos.r, pos.c, neighbor.direction)
            case Direction.WEST:
                if sketch[neighbor.r][neighbor.c] in ['-', 'F', 'L']:
                    return Position(pos.r, pos.c, neighbor.direction)
    raise ValueError("No start position found")


def next_position(pos: Position) -> Position:
    match pos.direction:
        case Direction.NORTH:
            return Position(pos.r - 1, pos.c)
        case Direction.EAST:
            return Position(pos.r, pos.c + 1)
        case Direction.SOUTH:
            return Position(pos.r + 1, pos.c)
        case Direction.WEST:
            return Position(pos.r, pos.c - 1)


def move(sketch: Map, pos: Position) -> Position:
    # Move to the next square and direction
    new_pos = next_position(pos)
    match pos.direction:
        case Direction.NORTH:
            match sketch[new_pos.r][new_pos.c]:
                case '|' | 'S':
                    return Position(new_pos.r, new_pos.c, Direction.NORTH)
                case 'F':
                    return Position(new_pos.r, new_pos.c, Direction.EAST)
                case '7':
                    return Position(new_pos.r, new_pos.c, Direction.WEST)
        case Direction.EAST:
            match sketch[new_pos.r][new_pos.c]:
                case '-' | 'S':
                    return Position(new_pos.r, new_pos.c, Direction.EAST)
                case 'J':
                    return Position(new_pos.r, new_pos.c, Direction.NORTH)
                case '7':
                    return Position(new_pos.r, new_pos.c, Direction.SOUTH)
        case Direction.SOUTH:
            match sketch[new_pos.r][new_pos.c]:
                case '|' | 'S':
                    return Position(new_pos.r, new_pos.c, Direction.SOUTH)
                case 'J':
                    return Position(new_pos.r, new_pos.c, Direction.WEST)
                case 'L':
                    return Position(new_pos.r, new_pos.c, Direction.EAST)
        case Direction.WEST:
            match sketch[new_pos.r][new_pos.c]:
                case '-' | 'S':
                    return Position(new_pos.r, new_pos.c, Direction.WEST)
                case 'L':
                    return Position(new_pos.r, new_pos.c, Direction.NORTH)
                case 'F':
                    return Position(new_pos.r, new_pos.c, Direction.SOUTH)


def puzzle1(sketch: list[str]) -> int:
    loc = find_start(sketch)
    logging.debug("Start point = %r", loc)
    pos = find_start_position(sketch, loc)
    logging.debug("Start = %r", pos)
    moves = 1
    pos = move(sketch, pos)
    logging.debug("Postion = %r", pos)
    while sketch[pos.r][pos.c] != 'S':
        pos = move(sketch, pos)
        logging.debug("Postion = %r", pos)
        moves += 1
    return moves // 2


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
