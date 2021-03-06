import argparse
import collections
import datetime
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


class Node:
    
    def __init__(self, license):
        self.nchildren = license.pop(0)
        self.nentries = license.pop(0)
        self.children = []
        self.mdentries = []
        for child in range(self.nchildren):
            self.children.append(Node(license))
        for e in range(self.nentries):
            self.mdentries.append(license.pop(0))
            

    def sum_metadata(self):
        child_sum = sum([c.sum_metadata() for c in self.children])
        return sum(self.mdentries) + child_sum


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    license = load_input(args.input)
    root = Node(license)
    logging.info('Root has nchildren: {}'.format(root.nchildren))
    logging.info('Root has children: {}'.format(root.children))
    logging.info('Root has nentries: {}'.format(root.nentries))
    logging.info('Root has entries: {}'.format(root.mdentries))
    metadata_sum = root.sum_metadata()
    print('Your answer is: {:d}'.format(metadata_sum))
        


if __name__ == '__main__':
    main(sys.argv)
