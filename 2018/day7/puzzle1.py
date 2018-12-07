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
    return [(line[5], line[36]) for line in fp]


def manhattan_distance(x1, y1, x2, y2):
    'See https://en.wikipedia.org/wiki/Taxicab_geometry'
    return abs(x1 - x2) + abs(y1 - y2)


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    arcs = collections.defaultdict(list)
    for a, b in load_input(args.input):
       arcs[a]
       arcs[b].append(a)

    for k, v in arcs.items():
        logging.debug('{}: {}'.format(k, v))

    steps = []
    while arcs:
        ready = sorted([k for k, v in arcs.items() if not v])
        logging.info('Ready: {}'.format(ready))
        step = ready[0]
        steps.append(step)
        del arcs[step]
        for v in arcs.values():
            try:
                v.remove(step)
            except ValueError as ve:
                pass
    print(''.join(steps))


if __name__ == '__main__':
    main(sys.argv)
