import argparse
import logging
import sys


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


def load_input(fp):
    data = []
    for line in fp:
        parts = line.split()
        verb = parts[0]
        amount = int(parts[1])
        data.append((verb, amount))
    return data


def puzzle1(commands) -> int:
    hpos = 0
    dpos = 0
    for verb, amount in commands:
        if verb == 'forward':
            hpos += amount
        elif verb == 'down':
            dpos += amount
        elif verb == 'up':
            dpos -= amount
    return hpos * dpos


def puzzle2(commands) -> int:
    hpos = 0
    dpos = 0
    aim = 0
    for verb, amount in commands:
        if verb == 'forward':
            hpos += amount
            dpos += aim * amount
        elif verb == 'down':
            aim += amount
        elif verb == 'up':
            aim -= amount
    return hpos * dpos


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    commands = load_input(args.input)
    answer = puzzle1(commands)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(commands)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main(sys.argv)
