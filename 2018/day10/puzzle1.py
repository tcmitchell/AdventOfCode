import argparse
import collections
import datetime
import itertools
import logging
import re
import sys
import time

# Time step 10459, message = NEXPLRXK


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
    return map(lambda s: map(int, re.findall(r'-?\d+', s)), fp)


Point = collections.namedtuple('Point', ['x', 'y', 'vx', 'vy'])


def step_time(points):
    return [Point(p.x + p.vx, p.y + p.vy, p.vx, p.vy) for p in points]


def display_points(points, xmin, ymin):
    grid = [['.'] * 200 for y in range(80)]
    for p in points:
        x = p.x - xmin
        y = p.y - ymin
        if 0 <= y < 80 and 0 <= x < 200:
            grid[y][x] = '#'
    for y in range(80):
        print(''.join(grid[y]))
    time.sleep(1)


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    points = load_input(args.input)
    points = [Point._make(p) for p in points]
    t = 0
    for i in range(11000):
        if t > 10400:
            xpts = [p.x for p in points]
            ypts = [p.y for p in points]
            xmin = min(xpts)
            xmax = max(xpts)
            ymin = min(ypts)
            ymax = max(ypts)
            rangex = xmax - xmin
            rangey = ymax - ymin
            if rangex < 200 and rangey < 80:
                display_points(points, xmin, ymin)
            logging.info('Time {}: {} x {} = {} area'.format(t, rangex, rangey, rangex * rangey))
            logging.info('xrange: {} ({} to {})'.format(xmax - xmin, xmin, xmax))
            logging.info('yrange: {} ({} to {})'.format(ymax - ymin, ymin, ymax))
        points = step_time(points)
        t += 1


if __name__ == '__main__':
    main(sys.argv)
