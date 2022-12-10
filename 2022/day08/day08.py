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


def load_input(fp: TextIO) -> list[list[int]]:
    data = []
    for line in fp.readlines():
        data.append([int(x) for x in list(line.strip())])
    return data


def tree_visible(r: int, c: int, forest: list[list[int]]) -> bool:
    """Determine if the tree at the given position is visible from the outside."""
    my_height = forest[r][c]
    l_neighbors = forest[r][:c]
    r_neighbors = forest[r][c+1:]
    u_neighbors = [forest[x][c] for x in range(r)]
    d_neighbors = [forest[x][c] for x in range(r+1, len(forest))]
    if (all((h < my_height for h in l_neighbors)) or
            all((h < my_height for h in r_neighbors)) or
            all(h < my_height for h in u_neighbors) or
            all(h < my_height for h in d_neighbors)):
        return True
    return False


def puzzle1(data: list[list[int]]) -> int:
    row_count = len(data)
    col_count = len(data[0])
    # visible = row_count * 2 + (col_count - 2) * 2
    visible = 0
    for r in range(row_count):
        for c in range(col_count):
            if tree_visible(r, c, data):
                visible += 1

    return visible


def scenic_score(r: int, c: int, forest: list[list[int]]) -> int:
    """Determine the scenic score of the tree at the given position."""
    my_height = forest[r][c]
    l_neighbors = forest[r][:c]
    r_neighbors = forest[r][c+1:]
    u_neighbors = [forest[x][c] for x in range(r)]
    d_neighbors = [forest[x][c] for x in range(r+1, len(forest))]
    # Reverse left and up neighbors, so we scan in the correct order
    l_neighbors.reverse()
    u_neighbors.reverse()
    score = 1
    for neighbors in (l_neighbors, r_neighbors, u_neighbors, d_neighbors):
        if not neighbors:
            # "If a tree is right on the edge, at least one of its
            #  viewing distances will be zero."
            return 0
        n_score = 0
        for tree_height in neighbors:
            n_score += 1
            if tree_height >= my_height:
                break
        score *= n_score
    return score


def puzzle2(data: list[list[int]]) -> int:
    # 9240 is too low
    row_count = len(data)
    col_count = len(data[0])
    max_score = 0
    ss = scenic_score(1, 2, data)
    print(f'Expected 4, got {ss}')
    ss = scenic_score(3, 2, data)
    print(f'Expected 8, got {ss}')
    for r in range(row_count):
        for c in range(col_count):
            ss = scenic_score(r, c, data)
            if ss > max_score:
                max_score = ss
    return max_score


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
