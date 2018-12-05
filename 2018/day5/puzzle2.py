import argparse
import collections
import datetime
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
    return fp.read().strip()


def match_test(a, b):
    return a != b and a.upper() == b.upper()


def remove_unit_pair(polymer):
    for i in range(len(polymer) - 1):
        if match_test(polymer[i], polymer[i+1]):
            del(polymer[i:i+2])
            return True
    return False


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    polymer = list(load_input(args.input))
    unique_units = set([x.upper() for x in polymer])
    lowest = (len(polymer), None)
    logging.info('There are {} unique units'.format(len(unique_units)))
    for uu in unique_units:
        logging.info('Removing all occurrences of unit {}'.format(uu))
        tmp_polymer = [p for p in polymer if p.upper() != uu]
        logging.info('Polymer length is now {}'.format(len(tmp_polymer)))
        while remove_unit_pair(tmp_polymer):
            pass
        tmp_len = len(tmp_polymer)
        print('Polymer final length is {} after removing {}'.format(tmp_len, uu))
        if tmp_len < lowest[0]:
            lowest = (tmp_len, uu)
        print('Shortest polymer is {} after removing {}'.format(lowest[0], lowest[1]))


if __name__ == '__main__':
    main(sys.argv)
