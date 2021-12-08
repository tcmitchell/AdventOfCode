from __future__ import annotations
import argparse
import logging
import sys
from typing import TextIO, Any, Tuple


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType('r'),
                        metavar="PUZZLE_INPUT")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    return args


def init_logging(debug=False):
    msgFormat = '%(asctime)s %(levelname)s %(message)s'
    dateFormat = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msgFormat, datefmt=dateFormat, level=level)


def load_input(fp: TextIO) -> list[Tuple[list[set], list[str]]]:
    result = []
    for line in fp:
        parts = line.split('|')
        parts = [p.strip() for p in parts]
        digits = [d.strip() for d in parts[1].split()]
        patterns = [set(p.strip()) for p in parts[0].split()]
        result.append((patterns, digits))
    return result


def puzzle1(data) -> int:
    # Extract just the digits portion of the data
    digits = [d[1] for d in data]
    target = [2, 4, 3, 7]
    total = 0
    for entry in digits:
        total += sum([1 for item in entry if len(item) in target])
    return total


def deduce_sixes(known: dict[int, set], patterns: list[set]) -> Any:
    assert 7 in known and 4 in known
    for pattern in patterns:
        plen = len(pattern)
        if plen == 6:
            match7 = len(known[7].intersection(pattern)) == len(known[7])
            match4 = len(known[4].intersection(pattern)) == len(known[4])
            if match7 and match4:
                known[9] = pattern
            elif match7 and not match4:
                known[0] = pattern
            elif not match7 and not match4:
                known[6] = pattern
            else:
                raise Exception('Unexpected match in sixes')


def deduce_fives(known: dict[int, set], patterns: list[set]) -> Any:
    assert 6 in known
    for pattern in patterns:
        plen = len(pattern)
        if plen == 5:
            match6 = len(known[6].intersection(pattern)) == 5
            match7 = len(known[7].intersection(pattern)) == len(known[7])
            if match6 and not match7:
                known[5] = pattern
            elif match7 and not match6:
                known[3] = pattern
            elif not match6 and not match7:
                known[2] = pattern
            else:
                raise Exception('Unexpected match in fives')


def deduce_patterns(patterns: list[set]) -> dict[int, set]:
    known = {}
    for pattern in patterns:
        plen = len(pattern)
        if plen == 2:
            known[1] = pattern
        elif plen == 4:
            known[4] = pattern
        elif plen == 3:
            known[7] = pattern
        elif plen == 7:
            known[8] = pattern
    deduce_sixes(known, patterns)
    deduce_fives(known, patterns)
    return known


def puzzle2(data: list[Tuple[list[set], list[str]]]) -> int:
    value = 0
    for d in data:
        known = deduce_patterns(d[0])
        lookup_table = {''.join(sorted(v)): k for k, v in known.items()}
        digits = [lookup_table[''.join(sorted(digit))] for digit in d[1]]
        readout = int(''.join([str(x) for x in digits]))
        logging.debug("%r -> %d", digits, readout)
        value += readout
    return value


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(data)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main(sys.argv)
