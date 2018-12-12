import argparse
import collections
import datetime
import itertools
import logging
import re
import sys
import time

# 500 17458
# 5000 179458
# 50000 1799458
# 50B 1799999999458


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
        # logging.debug('{} => {}'.format(pots, rules[pots]))
        return rules[pots]
    else:
        # logging.debug('{} => . *'.format(pots))
        return '.'


def sum_pots(pots, lpadding):
    potsum = 0
    for i in range(len(pots)):
        if pots[i] == '#':
            logging.debug('pot[{}] has a plant'.format(i - 20))
            potsum += i - lpadding
    return potsum


# The formula for predicting the value for a generation is:
#
#       (gen - 126) * 36 + 3994
#
# Since the generation index is zero based in the loop below,
# we only subtract 125 to account for that one off.
def predicted_sum(gen):
    return (gen - 125) * 36 + 3994


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    pots, rules = load_input(args.input)
    logging.info('pots: {}'.format(pots))
    logging.info('rules: {}'.format(rules))
    # Convert pots to a list so elements can be replaced
    pots = list(pots)

    lpadding = 0
    extension_size = 3
    # Maybe pad the pots on either side
    if '#' in pots[:3]:
        for i in range(extension_size):
            pots.insert(0, '.')
        lpadding += extension_size
    if '#' in pots[-3:]:
        pots.extend(['.'] * extension_size)

#    logging.debug(' 0: {}'.format(''.join(pots)))
    old_potsum = 0
    generations = 50000000000
    generations = 500
    # generations = 5000
    # generations = 50000
    # generations = 200
    for gen in range(generations):
        new_pots = [pots[0], pots[1]]
        for i in range(len(pots) - 4):
            new_pots.append(next_gen(rules, pots[i:i + 5]))
        new_pots.extend(pots[-2:])
        pots = new_pots

        potsum = sum_pots(pots, lpadding)
        logging.info('Gen {}: {} ({})'.format(gen, potsum,
                                              potsum - old_potsum))
        if gen > 125:
            predicted = predicted_sum(gen)
            if potsum == predicted:
                logging.info('{} == {}'.format(potsum, predicted))
            else:
                logging.warn('{} != {}'.format(potsum, predicted))
        old_potsum = potsum

        # Maybe pad the pots on either side
        if '#' in pots[:3]:
            for i in range(extension_size):
                pots.insert(0, '.')
            lpadding += extension_size
        if '#' in pots[-3:]:
            pots.extend(['.'] * extension_size)

        # if gen % 10000 == 0:
        #     logging.debug(gen)
        # logging.debug('{: >2d}: {}'.format(gen + 1, ''.join(pots)))

    logging.debug('pots length = {}'.format(len(pots)))
    potsum = 0
    for i in range(len(pots)):
        if pots[i] == '#':
            logging.debug('pot[{}] has a plant'.format(i - 20))
            potsum += i - lpadding
    print('Answer is {}'.format(potsum))


if __name__ == '__main__':
    main(sys.argv)
