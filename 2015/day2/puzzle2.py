#!/usr/bin/env python

import sys

def box_size(box_dims):
    b = [int(d) for d in box_dims.split('x')]
    b.sort()
    return (2*b[0] + 2*b[1] + b[0]*b[1]*b[2])

def load_data(filename):
    with open(filename, 'rb') as f:
        return sum([box_size(box) for box in f])

def main(argv=None):
    if not argv:
        argv = sys.argv
    print load_data(argv[1])

if __name__ == '__main__':
    main()
