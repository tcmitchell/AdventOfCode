#!/usr/bin/env python3

# http://adventofcode.com/2017/day/3

# Usage:
#    ./puzzle1.py 361527 | grep 361527
#   Sum the listed coordinates to get the Manhattan distance

import collections
import sys

grid = collections.defaultdict(int)


def fill(grid, target):
    ring = 1
    num = 1
    x = 0
    y = 0
    grid[(x, y)] = num
    num += 1
    while num < target:
        ring += 1
        x += 1
        # Right side
        for y in range(y, ring):
            grid[(x, y)] = num
            print('R grid[%d, %d] = %d' % (x, y, grid[(x, y)]))
            num += 1
        # Top side
        for x in range(x - 1, -ring, -1):
            grid[(x, y)] = num
            print('T grid[%d, %d] = %d' % (x, y, grid[(x, y)]))
            num += 1
        # Left side
        for y in range(y - 1, -ring, -1):
            grid[(x, y)] = num
            print('L grid[%d, %d] = %d' % (x, y, grid[(x, y)]))
            num += 1
        # Bottom side
        for x in range(x + 1, ring):
            grid[(x, y)] = num
            print('B grid[%d, %d] = %d' % (x, y, grid[(x, y)]))
            num += 1


def main(argv):
    target = int(argv[1])
    fill(grid, target)


if __name__ == '__main__':
    main(sys.argv)
