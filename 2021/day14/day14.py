from __future__ import annotations
import argparse
import collections
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


def load_input(fp: TextIO) -> Tuple[list[str], dict[Tuple[str, str], str]]:
    template = list(fp.readline().strip())
    fp.readline()
    rules = {}
    for line in fp:
        parts = line.strip().split(' -> ')
        rules[tuple(parts[0])] = parts[1]
    return template, rules


def step_polymer(template: list[str], rules: dict[Tuple[str, ...], str]) -> list[str]:
    pairs = [template[i:i+2] for i in range(len(template) - 1)]
    new_polymer = []
    for p in pairs:
        poly_insert = rules[tuple(p)]
        new_polymer.append(p[0])
        new_polymer.append(poly_insert)
    new_polymer.append(p[1])
    return new_polymer


def puzzle1(template: list[str], rules: dict[Tuple[str, ...], str]) -> int:
    polymer = template
    for i in range(10):
        polymer = step_polymer(polymer, rules)
        # logging.debug("Len %d: %s", len(polymer), ''.join(polymer))
    frequency = [(v, k) for k, v in collections.Counter(polymer).items()]
    most = max(frequency, key=lambda x: x[0])
    logging.debug("%s is most common at %d occurrences", most[1], most[0])
    least = min(frequency, key=lambda x: x[0])
    logging.debug("%s is least common at %d occurrences", least[1], least[0])
    return most[0] - least[0]


def puzzle2(template, rules) -> int:
    return 0

def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    template, rules = load_input(args.input)
    answer = puzzle1(template, rules)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(template, rules)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main()
