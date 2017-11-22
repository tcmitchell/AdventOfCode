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
    for i in range(10):
        print data[i]
    low = 0
    for _range in data:
        if _range[0] <= low + 1:
            if _range[1] > low:
                low = _range[1]
        else:
            break
    gap = low + 1
    print 'Gap at', gap

if __name__ == '__main__':
    main()
