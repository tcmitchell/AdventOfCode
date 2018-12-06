import argparse
import collections
import datetime
import logging
import sys


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType('r'),
                        metavar="PUZZLE_INPUT")
    parser.add_argument('limit', default=10000, nargs='?', type=int,
                        metavar="LIMIT")
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


Point = collections.namedtuple('Point', ['x', 'y'])


def load_input(fp):
    return [Point._make(map(int, line.strip().split(','))) for line in fp]


def manhattan_distance(x1, y1, x2, y2):
    'See https://en.wikipedia.org/wiki/Taxicab_geometry'
    return abs(x1 - x2) + abs(y1 - y2)


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    points = load_input(args.input)
    for p in points:
        logging.debug(p)

    # Scan for min/max of grid
    xpts = [p.x for p in points]
    ypts = [p.y for p in points]
    xmin = min(xpts)
    xmax = max(xpts) + 1
    ymin = min(ypts)
    ymax = max(ypts) + 1
    logging.info('x: {} to {}'.format(xmin, xmax))
    logging.info('y: {} to {}'.format(ymin, ymax))

    grid = []
    infinite_coords = set()
    max_dist = manhattan_distance(xmin, ymin, xmax, ymax) + 1
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            dist = sum([manhattan_distance(x, y, p.x, p.y) for p in points])
            if dist < args.limit:
                grid.append((x, y))
            
    print(len(grid))


if __name__ == '__main__':
    main(sys.argv)
