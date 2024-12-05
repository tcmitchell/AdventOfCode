from __future__ import annotations
import argparse
import logging
import math
import re
from collections import defaultdict
from functools import cmp_to_key
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


RULE_RE = re.compile(r'(\d+)\|(\d+)')

def load_input(fp: TextIO):
    rules = defaultdict(set)
    updates = []
    for line in fp:
        match = RULE_RE.match(line)
        if match:
            a = int(match.group(1))
            b = int(match.group(2))
            rules[a].add((a, b))
            rules[b].add((a, b))
            continue
        elif ',' in line:
            updates.append([int(x) for x in line.strip().split(',')])
    return rules, updates


def is_correct_order(rules: list[tuple[int, int]], update: list[int]) -> bool:
    for a, b in rules:
        if a in update and b in update:
            if update.index(a) > update.index(b):
                return False
    return True


def puzzle1(data) -> int:
    logger = logging.getLogger('puzzle1')
    rules, updates = data
    total = 0
    for update in updates:
        ruleset = []
        for page in update:
            ruleset.extend(rules[page])
        if is_correct_order(ruleset, update):
            logger.debug("Yes: %r", update)
            total += update[math.floor(len(update) / 2)]
        else:
            logger.debug("No: %r", update)
    return total


def order_update(rules: list[tuple[int, int]], update: list[int]) -> list[int]:
    def rule_cmp(a, b):
        if (a,b) in rules:
            return -1
        elif (b,a) in rules:
            return 1
        else:
            raise(ValueError(f"No rule for ({a}, {b})"))
    return sorted(update, key=cmp_to_key(rule_cmp))

def puzzle2(data) -> int:
    logger = logging.getLogger('puzzle1')
    rules, updates = data
    total = 0
    for update in updates:
        ruleset = []
        for page in update:
            ruleset.extend(rules[page])
        if not is_correct_order(ruleset, update):
            logger.debug("Yes: %r", update)
            update = order_update(ruleset, update)
            total += update[math.floor(len(update) / 2)]
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
