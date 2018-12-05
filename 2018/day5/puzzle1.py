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


# SLOW! works, but slowly. 35 seconds.
def remove_unit_pair(polymer):
    for i in range(len(polymer) - 1):
        if match_test(polymer[i], polymer[i+1]):
            del(polymer[i:i+2])
            return True
    return False


# FAST! 0.1 seconds.
def collapse(s):
    p = ['.']
    for u in s:
        v = p[-1]
        if v != u and v.lower() == u.lower():
            p.pop()
        else:
            p.append(u)
    return len(p) - 1


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    polymer = list(load_input(args.input))
    print(collapse(polymer))
    # print('Final polymer is {}'.format(polymer))
    # print('Polymer final length is {}'.format(len(polymer)))


if __name__ == '__main__':
    main(sys.argv)
