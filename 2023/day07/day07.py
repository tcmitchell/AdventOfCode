from __future__ import annotations
import argparse
import collections
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


CARD_VALUES1 = {c: i for i, c in enumerate(reversed('AKQJT98765432'))}
CARD_VALUES2 = {c: i for i, c in enumerate(reversed('AKQT98765432J'))}

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


def raw_hand_score(hand: str) -> tuple[int, ...]:
    counter = collections.Counter(hand)
    return tuple(sorted(counter.values()))

def score_hand1(hand: str) -> int:
    return HAND_VALUES[raw_hand_score(hand)]


def sort_key1(hand_wager: tuple[str, int]) -> tuple[int, ...]:
    key = [score_hand1(hand_wager[0])]
    key += [CARD_VALUES1[c] for c in hand_wager[0]]
    return tuple(key)


def handle3jokers(hand: str) -> int:
    subhand = hand.replace('J', '')
    raw_score = raw_hand_score(subhand)
    logging.debug("handle3: %s -> %s; %r", hand, subhand, raw_score)
    match raw_score:
        case (2,):
            return HAND_VALUES[(5,)]
        case(1, 1):
            return HAND_VALUES[(1, 4)]
    raise ValueError(f"Raw score {raw_score} of {hand} is not handled in handle3jokers")


def handle2jokers(hand: str) -> int:
    subhand = hand.replace('J', '')
    raw_score = raw_hand_score(subhand)
    logging.debug("handle2: %s -> %s; %r", hand, subhand, raw_score)
    match raw_score:
        case (3,):
            return HAND_VALUES[(5,)]
        case (1, 2):
            return HAND_VALUES[(1, 4)]
        case (1, 1, 1):
            return HAND_VALUES[(1, 1, 3)]
    raise ValueError(f"Raw score {raw_score} of {hand} is not handled in handle2jokers")


def handle1joker(hand: str) -> int:
    subhand = hand.replace('J', '')
    raw_score = raw_hand_score(subhand)
    logging.debug("handle1: %s -> %s; %r", hand, subhand, raw_score)
    match raw_score:
        case (4,):
            return HAND_VALUES[(5,)]
        case (1, 3):
            return HAND_VALUES[(1, 4)]
        case (2, 2):
            return HAND_VALUES[(2, 3)]
        case (1, 1, 2):
            return HAND_VALUES[(1, 1, 3)]
        case (1, 1, 1, 1):
            return HAND_VALUES[(1, 1, 1, 2)]
    raise ValueError(f"Raw score {raw_score} of {hand} is not handled in handle1jokers")


def score_hand2(hand: str) -> int:
    num_jokers = hand.count('J')
    match num_jokers:
        case 5:
            return HAND_VALUES[(5,)]
        case 4:
            # 4 jokers means 5 of a kind
            return HAND_VALUES[(5,)]
        case 3:
            return handle3jokers(hand)
        case 2:
            return handle2jokers(hand)
        case 1:
            return handle1joker(hand)
        case 0:
            return score_hand1(hand)
    raise ValueError(f"{num_jokers} jokers is not handled in hand {hand}")


def puzzle1(data: list[tuple[str, int]]) -> int:
    hands = sorted(data, key=sort_key1)
    total = 0
    for i, hand_wager in enumerate(hands, start=1):
        hand, wager = hand_wager
        total += wager * i
        logging.debug("Hand %s, wager %d; key = %r", hand, wager, sort_key1((hand, wager)))
    return total


def sort_key2(hand_wager: tuple[str, int]) -> tuple[int, ...]:
    key = [score_hand2(hand_wager[0])]
    key += [CARD_VALUES2[c] for c in hand_wager[0]]
    return tuple(key)


def puzzle2(data) -> int:
    hands = sorted(data, key=sort_key2)
    total = 0
    for i, hand_wager in enumerate(hands, start=1):
        hand, wager = hand_wager
        total += wager * i
        logging.debug("Hand %s, wager %d; key = %r", hand, wager, sort_key1((hand, wager)))
    return total


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
