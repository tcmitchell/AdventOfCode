from __future__ import annotations
import argparse
import logging
import re
from collections.abc import Collection, Iterable
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


DIGIT_RE = re.compile(r'\d')

def puzzle1(data) -> int:
    total = 0
    for line in data:
        digits = DIGIT_RE.findall(line)
        code = int("".join([digits[0], digits[-1]]))
        print(code)
        total += code
    return total


digit_strings = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

DIGITS_RE = re.compile("|".join(list(digit_strings.keys()) + list(digit_strings.values())))

for v in list(digit_strings.values()):
    digit_strings[v] = v

def find_overlapping(pattern: re.Pattern[str], input: str) -> Iterable[str]:
    m = pattern.search(input, 0)
    while m is not None:
        yield m.group(0)
        m = pattern.search(input, m.start() + 1)

# 438597 is too high
# 54232 is too low
# 54251 is wrong
# 54249 is correct
def puzzle2(data: Collection[str]) -> int:
    data2 = []
    for d in data:
        m = [digit_strings[token] for token in find_overlapping(DIGITS_RE, d)]
        data2.append("".join(m))
    return puzzle1(data2)


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    # answer = puzzle1(data)
    # logging.info('Puzzle 1: %r', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %r', answer)


if __name__ == '__main__':
    main()
