import argparse
import collections
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


def claim_re():
    regex = r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$'
    return re.compile(regex)


def parse_claim(regex, claim):
    match = regex.match(claim)
    return (int(x) for x in match.groups())


def process_claim(fabric, claim_regex, raw_claim):
    parsed_claim = parse_claim(claim_regex, raw_claim)
    claim_id, left, top, width, height = parsed_claim
    logging.debug('Claim {} @ {},{}: {}x{}'.format(claim_id, left, top, width, height))
    for x in range(left, left+width):
        for y in range(top, top+height):
            fabric[x, y].append(claim_id)


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    fabric = collections.defaultdict(list)
    claim_regex = claim_re()
    for line in args.input:
        process_claim(fabric, claim_regex, line.strip())
    overlaps = collections.defaultdict(bool)
    for v in fabric.values():
        is_overlap = len(v) > 1
        for claim in v:
            overlaps[claim] = overlaps[claim] or is_overlap
    logging.debug(overlaps)
    for claim, is_overlap in overlaps.items():
        logging.debug('{}: {}'.format(claim, is_overlap))
        if not is_overlap:
            print('Claim {} has no overlaps'.format(claim))


if __name__ == '__main__':
    main(sys.argv)
