import argparse
import collections
import datetime
import itertools
import logging
import re
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
    return list(map(int, re.findall(r'-?\d+', fp.read())))


def insert_marble(ring, current_marble, new_marble):
    ring.rotate(- ring.index(current_marble))
    ring.rotate(-2)
    ring.insert(0, new_marble)
#    ring.rotate(- ring.index(0))


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    (nelves, nmarbles) = load_input(args.input)
    nmarbles += 1
    logging.info('{} elves, {} marbles'.format(nelves, nmarbles))
    elves = itertools.cycle(range(1, nelves + 1))
    score = collections.defaultdict(int)
    current_marble = 0
    ring = collections.deque([0])
    for elf, marble in zip(elves, range(1, nmarbles)):
        if marble % 1000 == 0:
            logging.info('Elf {} plays marble {}'.format(elf, marble))
        if marble % 23 == 0:
            score[elf] += marble
            ring.rotate(- ring.index(current_marble))
            ring.rotate(6)
            score[elf] += ring.pop()
            current_marble = ring[0]
            # logging.info('Current marble is now {}'.format(current_marble))
            # ring.rotate(- ring.index(0))
        else:
            insert_marble(ring, current_marble, marble)
            current_marble = marble
        # logging.debug('Ring: {}'.format(ring))
    print('high score is {}'.format(max(score.values())))


if __name__ == '__main__':
    main(sys.argv)
