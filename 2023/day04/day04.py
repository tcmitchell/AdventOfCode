from __future__ import annotations
import argparse
import logging
import re
from collections.abc import Collection
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


PARSE_LINE_RE = re.compile(r"Card\s*(\d+):([\s\d]*)\|([\s\d]*)")
ALL_INTS_RE = re.compile(r"\d+")

def load_input(fp: TextIO) -> Collection[tuple[int, Collection[int], Collection[int]]]:
    data = []
    for line in fp:
        match = PARSE_LINE_RE.match(line)
        if match is None:
            raise ValueError(f"Cannot parse {line}")
        data.append((int(match.group(1)),
                     [int(x) for x in ALL_INTS_RE.findall(match.group(2))],
                     [int(x) for x in ALL_INTS_RE.findall(match.group(3))]))
    return data


def puzzle1(data: Collection[tuple[int, Collection[int], Collection[int]]]) -> int:
    total_points = 0
    for _, winning, mine in data:
        matched_numbers = [True for n in mine if n in winning]
        if not matched_numbers:
            continue
        points = 2 ** (len(matched_numbers) - 1)
        total_points += points
    return total_points


def puzzle2TooSlow(data: Collection[tuple[int, Collection[int], Collection[int]]]) -> int:
    total_cards = 0
    card_lookup = {card[0]: card for card in data}
    card_stack = list(data)
    while card_stack:
        card = card_stack.pop(0)
        idx, winning, mine = card
        match_count = len([True for n in mine if n in winning])
        for i in range(idx+1, idx+match_count+1):
            card_stack.append(card_lookup[i])
        total_cards += 1
    return total_cards


def puzzle2(data: Collection[tuple[int, Collection[int], Collection[int]]]) -> int:
    # Loop backwards through the cards computing how many cards each will win
    card_lookup: dict[int, int] = {}
    for idx, winning, mine in reversed(list(data)):
        logging.debug("Precomputing card %d", idx)
        match_count = len([True for n in mine if n in winning])
        cards_won = match_count + sum([card_lookup[i] for i in range(idx+1, idx+match_count+1)])
        card_lookup[idx] = cards_won
    # Now figure out how many total cards
    total_cards = sum(card_lookup.values()) + len(card_lookup)
    return total_cards


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
