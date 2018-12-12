import argparse
import collections
import datetime
import itertools
import logging
import re
import sys
import time

# Right: 1696

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
    pots = fp.readline().strip().split()[2]
    fp.readline()
    rules = [line.strip().split() for line in fp]
    rules = {r[0]: r[2] for r in rules}
    return pots, rules


def next_gen(rules, pots):
    pots = ''.join(pots)
    if pots in rules:
#        logging.debug('{} => {}'.format(pots, rules[pots]))
        return rules[pots]
    else:
#        logging.debug('{} => . *'.format(pots))
        return '.'


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    pots, rules = load_input(args.input)
    logging.info('pots: {}'.format(pots))
    logging.info('rules: {}'.format(rules))
    # Pad the pots on either side
    padding = 20
    pots = '.' * padding + pots + '.' * padding
    pots = list(pots)
    plants = 0
    logging.debug(' 0: {}'.format(''.join(pots)))
    for gen in range(20):
        new_pots = [pots[0], pots[1]]
        for i in range(len(pots) - 4):
            new_pots.append(next_gen(rules, pots[i:i + 5]))
        new_pots.extend(pots[-2:])
        pots = new_pots
        plants += pots.count('#')
        logging.debug('{: >2d}: {}  ({})'.format(gen + 1, ''.join(pots), plants))
    potsum = 0
    for i in range(len(pots)):
        if pots[i] == '#':
            logging.debug('pot[{}] has a plant'.format(i - 20))
            potsum += i - 20
    print('Answer is {}'.format(potsum))


if __name__ == '__main__':
    main(sys.argv)
