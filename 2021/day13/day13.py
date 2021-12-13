from __future__ import annotations
import argparse
import logging
from typing import TextIO, Tuple


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


def load_input(fp: TextIO) -> Tuple[set[Tuple[int, int]], list[Tuple[str, int]]]:
    dots = set()
    folds = []
    for line in fp:
        line = line.strip()
        if line.startswith('fold along '):
            parts = line.split('=')
            folds.append((parts[0][-1], int(parts[1])))
        elif ',' in line:
            parts = line.split(',')
            dots.add((int(parts[0]), int(parts[1])))
    return dots, folds


def fold_horizontal(fold_line: int, dots: set[Tuple[int, int]]) -> set[Tuple[int, int]]:
    result = set()
    for x, y in dots:
        if y < fold_line:
            result.add((x, y))
        else:
            y = fold_line - (y - fold_line)
            result.add((x, y))
    return result


def fold_vertical(fold_line: int, dots: set[Tuple[int, int]]) -> set[Tuple[int, int]]:
    result = set()
    for x, y in dots:
        if x < fold_line:
            result.add((x, y))
        else:
            x = fold_line - (x - fold_line)
            result.add((x, y))
    return result


def fold(axis: str, fold_line: int, dots: set[Tuple[int, int]]) -> set[Tuple[int, int]]:
    if axis == 'y':
        return fold_horizontal(fold_line, dots)
    elif axis == 'x':
        return fold_vertical(fold_line, dots)


def puzzle1(dots: set[Tuple[int, int]], folds: list[Tuple[str, int]]) -> int:
    axis, fold_line = folds[0]
    dots = fold(axis, fold_line, dots)
    return len(dots)


def puzzle2(dots: set[Tuple[int, int]], folds: list[Tuple[str, int]]) -> int:
    logging.debug("Starting with %d dots", len(dots))
    for axis, fold_line in folds:
        dots = fold(axis, fold_line, dots)
        logging.debug("Folded to %d dots", len(dots))
    max_x = max([x for x, y in dots])
    max_y = max([y for x, y in dots])
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x, y) in dots:
                print('#', end='')
            else:
                print('.', end='')
        print('')
    return 0


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    dots, folds = load_input(args.input)
    answer = puzzle1(dots, folds)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(dots, folds)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main()
