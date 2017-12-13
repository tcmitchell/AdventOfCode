#!/usr/bin/env python3

# http://adventofcode.com/2017/day/13

import sys


def parse_line(input_line):
    return tuple([int(x) for x in input_line.split(b':')])


def load_input(datafile):
    with open(datafile, 'rb') as f:
        return [parse_line(l) for l in f.readlines()]


def main(argv):
    datafile = argv[1]
    data = load_input(datafile)
    print(data)
    severity = 0
    for (d, r) in data:
        # Compute number of positions for scanner
        p = max(r, r + r - 2)
        print('Depth %d has %d positions' % (d, p))
        print('Depth %d scanner is at position %d' % (d, d % p))
        if d % p == 0:
            severity += d * r
    print('Severity = %d' % (severity))


if __name__ == '__main__':
    main(sys.argv)
