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


def load_input(fp: TextIO) -> list[tuple[str, int]]:
    result = [(d, int(c)) for d, c in
              (line.split() for line in fp.readlines())]
    return result


class Knot:

    def __init__(self, x: int = 0, y: int = 0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'#<Knot x:{self.x} y:{self.y}>'

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy


UP = 'U'
DOWN = 'D'
RIGHT = 'R'
LEFT = 'L'

MOVE_DELTAS = dict(U=(0, 1), D=(0, -1), L=(-1, 0), R=(1, 0))


def adjacent(head: Knot, tail: Knot) -> bool:
    """Determine if tail is adjacent to head."""
    return abs(tail.x - head.x) < 2 and abs(tail.y - head.y) < 2


def move_tail(head: Knot, tail: Knot, dx: int, dy: int):
    """Adjust tail position to be adjacent to head."""
    if head.x == tail.x:
        # Adjust in y
        tail.move(0, dy)
    elif head.y == tail.y:
        # Adjust in x
        tail.move(dx, 0)
    else:
        # Adjust diagonally
        pass

def move(head: Knot, tail: Knot, dx: int, dy: int):
    """Move the head and possibly the tail, by delta_row, delta_column."""
    head.move(dx, dy)
    if adjacent(head, tail):
        print(f'Adjacent: {head}, {tail}')
    else:
        print(f'Not Adjacent: {head}, {tail}')
        move_tail(head, tail, dx, dy)
        if not adjacent(head, tail):
            raise Exception("Not adjacent after moving tail")


def puzzle1(data: list[tuple[str, int]]) -> int:
    head = Knot()
    tail = Knot()
    for move_dir, move_count in data:
        dx, dy = MOVE_DELTAS[move_dir]
        for i in range(move_count):
            move(head, tail, dx, dy)
    return 0


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
