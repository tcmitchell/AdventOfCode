from __future__ import annotations
import argparse
import logging
from typing import TextIO, List, Tuple


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


def load_input(fp: TextIO) -> list[list[str]]:
    rounds = (line.strip() for line in fp.readlines())
    return [rond.split() for rond in rounds]


ROCK = 'R'
PAPER = 'P'
SCISSORS = 'S'

PLAY_TABLE = {ROCK: 1, PAPER: 2, SCISSORS: 3}


def translate_guide(guide: list[list[str]], tbl: dict[str, str]) -> list[list[str]]:
    return [[tbl[item] for item in rond] for rond in guide]


def translate_guide2(guide: list[list[str]], tbl: dict[str, str]) -> list[list[str]]:
    lose_tbl = {ROCK: SCISSORS, PAPER: ROCK, SCISSORS: PAPER}
    win_tbl = {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}
    result = []
    for them, outcome in guide:
        them = tbl[them]
        if outcome == 'X':
            # Lose
            result.append([them, lose_tbl[them]])
        elif outcome == 'Y':
            # Draw
            result.append([them, them])
        elif outcome == 'Z':
            # Win
            result.append([them, win_tbl[them]])
    return result


def score_round(them: str, us: str) -> int:
    score = PLAY_TABLE[us]
    if them == ROCK:
        if us == ROCK:
            score += 3  # Draw
        elif us == PAPER:
            score += 6  # Win
    elif them == PAPER:
        if us == PAPER:
            score += 3  # Draw
        elif us == SCISSORS:
            score += 6  # Win
    elif them == SCISSORS:
        if us == SCISSORS:
            score += 3  # Draw
        elif us == ROCK:
            score += 6  # Win
    return score


def score_rounds(rps_guide: list[list[str]]) -> list[int]:
    return [score_round(*rond) for rond in rps_guide]


def puzzle1(data) -> int:
    trans_table = dict(A=ROCK, B=PAPER, C=SCISSORS,
                       X=ROCK, Y=PAPER, Z=SCISSORS)
    rounds = translate_guide(data, trans_table)
    scores = score_rounds(rounds)
    return sum(scores)


def puzzle2(data) -> int:
    trans_table = dict(A=ROCK, B=PAPER, C=SCISSORS,
                       X=ROCK, Y=PAPER, Z=SCISSORS)
    rounds = translate_guide2(data, trans_table)
    scores = score_rounds(rounds)
    return sum(scores)


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(data)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main()
