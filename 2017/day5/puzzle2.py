#!/usr/bin/env python3

# http://adventofcode.com/2017/day/5

import sys


def load_jumps(datafile):
    with open(datafile, 'rb') as f:
        return [int(line) for line in f]


def execute(jumps, ptr):
    offset = jumps[ptr]
    if offset >= 3:
        jumps[ptr] -= 1
    else:
        jumps[ptr] += 1
    return ptr + offset


def main(argv):
    datafile = argv[1]
    jumps = load_jumps(datafile)
    jump_len = len(jumps)
    steps = 0
    ptr = 0
    while ptr >= 0 and ptr < jump_len:
        ptr = execute(jumps, ptr)
        steps += 1
        # print('ptr=%d; %r' % (ptr, jumps))
    print('It took %d steps to leave the program.' % (steps))


if __name__ == '__main__':
    main(sys.argv)
