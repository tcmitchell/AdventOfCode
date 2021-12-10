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


def load_input(fp: TextIO):
    return [line.strip() for line in fp.readlines()]


# ): 3 points.
# ]: 57 points.
# }: 1197 points.
# >: 25137 points.
CHAR_SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}
OPEN_CHARS = ['(', '[', '{', '<']
CLOSE_CHARS = CHAR_SCORES.keys()
MATCH_CLOSE_OPEN = {')': '(', ']': '[', '}': '{', '>': '<'}
MATCH_OPEN_CLOSE = {v: k for k, v in MATCH_CLOSE_OPEN.items()}
CHAR_SCORES2 = {')': 1, ']': 2, '}': 3, '>': 4}


def check_syntax(line: str) -> int:
    stack = []
    for char in line:
        if char in OPEN_CHARS:
            stack.append(char)
        elif char in CLOSE_CHARS:
            match = stack.pop()
            if MATCH_CLOSE_OPEN[char] != match:
                # Syntax Error
                return CHAR_SCORES[char]
        else:
            raise Exception(f"Unknown char {char}")
    return 0


def puzzle1(data) -> Tuple[int, list[str]]:
    score = 0
    incomplete = []
    for line in data:
        line_score = check_syntax(line)
        score += line_score
        if line_score == 0:
            incomplete.append(line)
    return score, incomplete


def puzzle2(data) -> int:
    all_scores = []
    for line in data:
        stack = []
        score = 0
        for char in line:
            if char in OPEN_CHARS:
                stack.append(char)
            elif char in CLOSE_CHARS:
                stack.pop()
        while stack:
            char = stack.pop()
            assert char in OPEN_CHARS
            score *= 5
            score += CHAR_SCORES2[MATCH_OPEN_CLOSE[char]]
        all_scores.append(score)
    all_scores.sort()
    logging.debug("all scores: %r", all_scores)
    middle = len(all_scores) // 2
    return all_scores[middle]


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer, incomplete = puzzle1(data)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(incomplete)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main()
