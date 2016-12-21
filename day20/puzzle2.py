#!/usr/bin/env python

import sys

def load_data(infile):
    with open(infile, 'rb') as f:
        return [[int(x) for x in l.strip().split('-')] for l in f]

def main(argv=None):
    if not argv:
        argv = sys.argv
    infile = argv[1]
    data = load_data(infile)
    data.sort()
    max_ip = 4294967295
    # max_ip = 10
    white = []
    low = 0
    for _range in data:
        while low+1 < _range[0] and low+1 <= max_ip:
            print 'whitelisting', low+1, 'range =', _range
            white.append(low+1)
            low += 1
        if _range[1] > low:
            low = _range[1]
    print 'Whitelist length', len(white)

# 272 is too high
# 109 is correct

if __name__ == '__main__':
    main()
