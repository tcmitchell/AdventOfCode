import argparse
import logging
import sys
from collections import defaultdict


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
    return [line.strip() for line in fp]


def puzzle1(data) -> int:
    gamma_list = []
    epsilon_list = []
    for i in range(len(data[0])):
        logging.debug('i = %r', i)
        tally = defaultdict(int)
        for item in data:
            tally[item[i]] += 1
        if tally['1'] > tally['0']:
            gamma_list.append('1')
            epsilon_list.append('0')
        else:
            gamma_list.append('0')
            epsilon_list.append('1')
    logging.debug('gamma_list = %r', gamma_list)
    logging.debug('epsilon_list = %r', epsilon_list)
    gamma = int(''.join(gamma_list), base=2)
    epsilon = int(''.join(epsilon_list), base=2)
    return gamma * epsilon


def puzzle2(commands) -> int:
    return 0


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
