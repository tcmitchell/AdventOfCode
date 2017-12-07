#!/usr/bin/env python3

# http://adventofcode.com/2017/day/5

import sys


def load_input(datafile):
    with open(datafile, 'rb') as f:
        return [line.decode('utf-8').rstrip() for line in f]


def parse_input(raw_data, programs, supported):
    """The lines take two forms:

    1. name (###)
    2. name (###) -> name, name, name
    """
    for line in raw_data:
        x = line.split('->')
        prog = x[0].split()[0]
        programs.append(prog)
        # print(prog)
        if len(x) > 1:
            sup = [n.strip() for n in x[1].split(',')]
            supported.extend(sup)


def main(argv):
    datafile = argv[1]
    raw_data = load_input(datafile)
    programs = []
    supported = []
    parse_input(raw_data, programs, supported)
    for p in programs:
        if p not in supported:
            print('Not supported: %r' % (p))


if __name__ == '__main__':
    main(sys.argv)
