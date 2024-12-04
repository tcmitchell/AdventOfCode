from __future__ import annotations
import argparse
import logging
from collections import defaultdict
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


def countFH(word: str, data: list[str]) -> int:
    count = 0
    for row in data:
        count += row.count(word)
    return count


def countRH(word: str, data: list[str]) -> int:
    word = "".join(reversed(word))
    count = 0
    for row in data:
        count += row.count(word)
    return count


def countDV(word: str, data: list) -> int:
    count = 0
    for i in range(len(data[0])):
        count += "".join([line[i] for line in data]).count(word)
    return count


def countUV(word: str, data: list) -> int:
    count = 0
    for i in range(len(data[0])):
        count += "".join(reversed([line[i] for line in data])).count(word)
    return count


def get_diagonal(data: list[str], i: int, j: int) -> str:
    if j < 0 or j >= len(data):
        return ""
    elif i < 0 or i >= len(data[0]):
        return ""
    else:
        return data[j][i]


def countDRD(word: str, data: list) -> int:
    diagonals = []
    for i in range(-len(data[0]), 2 * len(data[0])):
        diag = []
        for j in range(len(data)):
            diag.append(get_diagonal(data, i+j, i+j))
        diagonals.append("".join(diag))
    count = 0
    for diagonal in diagonals:
        count += diagonal.count(word)
    return count


# https://stackoverflow.com/a/43311126
def groups(data, func):
    grouping = defaultdict(list)
    for y in range(len(data)):
        for x in range(len(data[y])):
            grouping[func(x, y)].append(data[y][x])
    return list(map(grouping.get, sorted(grouping)))


def puzzle1(data: list[str]) -> int:
    word = "XMAS"
    count = 0
    cols = groups(data, lambda x, y: x)
    rows = groups(data, lambda x, y: y)
    fdiag = groups(data, lambda x, y: x + y)
    bdiag = groups(data, lambda x, y: x - y)

    for group in (cols, rows, fdiag, bdiag):
        count += sum(["".join(x).count(word) for x in group])
        count += sum(["".join(reversed(x)).count(word) for x in group])
    return count


def is_x_mas(data: list[str], r: int, c: int) -> bool:
    m_or_s = ("M", "S")
    up_left = data[r-1][c-1]
    down_right = data[r+1][c+1]
    up_right = data[r-1][c+1]
    down_left = data[r+1][c-1]
    # print("------")
    # print(f"R: {r}, C: {c}")
    # print(data[r-1][c-1:c+2])
    # print(data[r][c - 1:c + 2])
    # print(data[r + 1][c - 1:c + 2])
    if up_left in m_or_s and down_right in m_or_s and up_left != down_right:
        if up_right in m_or_s and down_left in m_or_s and up_right != down_left:
            # print("yes")
            return True
    # print("no")
    return False


def puzzle2(data: list[str]) -> int:
    count = 0
    for r in range(1, len(data) - 1):
        for c in range(1, len(data[r]) - 1):
            if data[r][c] == "A":
                count += is_x_mas(data, r, c)
    return count


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
