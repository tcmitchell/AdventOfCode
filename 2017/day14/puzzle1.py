#!/usr/bin/env python3

# http://adventofcode.com/2017/day/10

import sys

import knothash

GRID_SIZE = 128


# Data is all on one line
def load_input(datafile):
    with open(datafile, 'rb') as f:
        return f.read().rstrip()


def to_bin(kh):
    # knothashes are hex
    scale = 16
    # each hex character in a knothash represents 4 bits
    num_of_bits = len(kh) * 4
    return bin(int(kh, scale))[2:].zfill(num_of_bits)


def count_used(kh):
    return to_bin(kh).count('1')


def main(argv):
    # knothash.test()
    datafile = argv[1]
    key_string = load_input(datafile)
    used_blocks = 0
    for i in range(GRID_SIZE):
        key = key_string + b'-' + bytes(str(i), 'utf-8')
        aoc_hash = knothash.knothash(key)
        # print('Hash for %r: %r' % (key, aoc_hash))
        # print('\t%r' % (to_bin(aoc_hash)))
        used_blocks += count_used(aoc_hash)
    print('There are %d used blocks' % (used_blocks))


if __name__ == '__main__':
    main(sys.argv)
