from __future__ import annotations
import argparse
import collections
import itertools
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


ALL_TOKENS_RE = re.compile("\w+")

def load_input(fp: TextIO) -> list[tuple[str, int]]:
    data = []
    for line in fp:
        tokens = ALL_TOKENS_RE.findall(line)
        data.append((tokens[0], int(tokens[1])))
    return data


CARD_VALUES = {c: i for i, c in enumerate(reversed('AKQJT98765432'))}

ALL_HAND_VALUES = [
    (5,),  # Five of a kind
    (1, 4),  # Four of a kind
    (2, 3),  # Full House
    (1, 1, 3),  # Three of a kind
    (1, 2, 2),  # Two pair
    (1, 1, 1, 2),  # One pair
    (1, 1, 1, 1, 1),  # High card
]
HAND_VALUES = {h: i for i, h in enumerate(reversed(ALL_HAND_VALUES))}


def score_hand(hand: str) -> int:
    counter = collections.Counter(hand)
    occurrences = tuple(sorted(counter.values()))
    return HAND_VALUES[occurrences]


def sort_key1(hand_wager: tuple[str, int]) -> tuple[int, ...]:
    key = [score_hand(hand_wager[0])]
    key += [CARD_VALUES[c] for c in hand_wager[0]]
    return tuple(key)

def puzzle1(data: list[tuple[str, int]]) -> int:
    hands = sorted(data, key=sort_key1)
    total = 0
    for i, hand_wager in enumerate(hands, start=1):
        hand, wager = hand_wager
        total += wager * i
        logging.debug("Hand %s, wager %d; key = %r", hand, wager, sort_key1((hand, wager)))
    return total


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
