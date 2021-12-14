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


def load_input(fp: TextIO) -> Tuple[str, dict[str, Tuple[str, str]]]:
    template = fp.readline().strip()
    fp.readline()
    rules = {}
    for line in fp:
        parts = line.strip().split(' -> ')
        rules[parts[0]] = (parts[0][0] + parts[1], parts[1] + parts[0][1])
    return template, rules


def template2polymer(template: str) -> dict[str, int]:
    polymer = collections.defaultdict(int)
    for i in range(len(template) - 1):
        polymer[template[i:i+2]] += 1
    return polymer


def step_polymer(template: dict[str, int], rules: dict[str, Tuple[str, str]]) -> dict[str, int]:
    new_polymer = collections.defaultdict(int)
    for k, v in template.items():
        for poly in rules[k]:
            new_polymer[poly] += v
    return new_polymer


def count_chars(polymer: dict[str, int], bonus: list[str]):
    counter = collections.defaultdict(int)
    for k, v in polymer.items():
        for c in k:
            counter[c] += v
    for b in bonus:
        counter[b] += 1
    for k, v in counter.items():
        counter[k] = v // 2
    return counter


def puzzle1(template: str, rules: dict[str, Tuple[str, str]]) -> int:
    polymer = template2polymer(template)
    bonus = [template[0], template[-1]]
    for i in range(10):
        polymer = step_polymer(polymer, rules)
        # logging.debug("Freqs: %r", count_chars(polymer, bonus))
        # logging.debug("Len %d: %s", len(polymer), ''.join(polymer))

    frequency = [(v, k) for k, v in count_chars(polymer, bonus).items()]
    most = max(frequency, key=lambda x: x[0])
    logging.debug("%s is most common at %d occurrences", most[1], most[0])
    least = min(frequency, key=lambda x: x[0])
    logging.debug("%s is least common at %d occurrences", least[1], least[0])
    return most[0] - least[0]
    # return 0


def puzzle2(template: str, rules: dict[str, Tuple[str, str]]) -> int:
    polymer = template2polymer(template)
    bonus = [template[0], template[-1]]
    for i in range(40):
        polymer = step_polymer(polymer, rules)
        # logging.debug("Freqs: %r", count_chars(polymer, bonus))
        # logging.debug("Len %d: %s", len(polymer), ''.join(polymer))

    frequency = [(v, k) for k, v in count_chars(polymer, bonus).items()]
    most = max(frequency, key=lambda x: x[0])
    logging.debug("%s is most common at %d occurrences", most[1], most[0])
    least = min(frequency, key=lambda x: x[0])
    logging.debug("%s is least common at %d occurrences", least[1], least[0])
    return most[0] - least[0]


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
