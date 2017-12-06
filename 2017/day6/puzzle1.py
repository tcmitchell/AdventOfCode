#!/usr/bin/env python

# http://adventofcode.com/2017/day/6

import sys


def load_data(datafile):
    with open(datafile, 'rb') as f:
        return [int(item) for item in [line.split('\t') for line in f][0]]


def most_blocks(banks):
    "Find the bank with the most blocks. Return the index of that bank."
    # There's probably a one-liner to do this...
    most_index = 0
    most = banks[0]
    for i in range(1, len(banks)):
        if banks[i] > most:
            most = banks[i]
            most_index = i
    return most_index


def next_bank_id(banks, bank_id):
    bank_id += 1
    if bank_id >= len(banks):
        bank_id = 0
    return bank_id

def realloc(banks, bank_id):
    "Reallocate the blocks in bank[bank_id] in the spirit of Mancala"
    blocks = banks[bank_id]
    banks[bank_id] = 0
    while blocks > 0:
        bank_id = next_bank_id(banks, bank_id)
        banks[bank_id] += 1
        blocks -= 1

def main(argv):
    datafile = argv[1]
    banks = load_data(datafile)
    memory = []
    reallocs = 0
    while banks not in memory:
        memory.append(list(banks))
        realloc(banks, most_blocks(banks))
        reallocs += 1
    # print 'Most blocks in bank %d' % (most_blocks(banks))
    print 'Performed %d reallocs' % (reallocs)


if __name__ == '__main__':
    main(sys.argv)
