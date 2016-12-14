#!/usr/bin/env python

import sys
from collections import defaultdict


def load_data(filename):
    with open(filename, 'rb') as f:
        return f.read()

def main(argv=None):
    if not argv:
        argv = sys.argv
    instructions = load_data(argv[1])
    visited = defaultdict(lambda:0)
    x = 0
    y = 0
    visited[(x, y)] = 1
    for i in instructions:
        if i == '^':
            y += 1
        elif i == 'v':
            y -= 1
        elif i == '>':
            x += 1
        elif i == '<':
            x -= 1
        else:
            continue
        visited[(x, y)] += 1
    print len(visited)

if __name__ == '__main__':
    main()
