#!/usr/bin/env python3

# http://adventofcode.com/2017/day/3

# Usage:
#    ./puzzle1.py 361527 | grep 361527
#   Sum the listed coordinates to get the Manhattan distance

import collections
import sys

grid = collections.defaultdict(int)


def sum_neighbors(grid, x, y):
    return sum([grid[(x - 1, y - 1)],
                grid[(x - 1, y)],
                grid[(x - 1, y + 1)],
                grid[(x,     y + 1)],
                grid[(x + 1, y + 1)],
                grid[(x + 1, y)],
                grid[(x + 1, y - 1)],
                grid[(x,     y - 1)]
                ])


def fill(grid, target):
    ring = 1
    x = 0
    y = 0
    grid[(x, y)] = 1
    while sum_neighbors(grid, x, y) < target:
        ring += 1
        x += 1
        # Right side
        for y in range(y, ring):
            grid[(x, y)] = sum_neighbors(grid, x, y)
            print('R grid[%d, %d] = %d' % (x, y, grid[(x, y)]))
        # Top side
        for x in range(x - 1, -ring, -1):
            grid[(x, y)] = sum_neighbors(grid, x, y)
            print('T grid[%d, %d] = %d' % (x, y, grid[(x, y)]))
        # Left side
        for y in range(y - 1, -ring, -1):
            grid[(x, y)] = sum_neighbors(grid, x, y)
            print('L grid[%d, %d] = %d' % (x, y, grid[(x, y)]))
        # Bottom side
        for x in range(x + 1, ring):
            grid[(x, y)] = sum_neighbors(grid, x, y)
            print('B grid[%d, %d] = %d' % (x, y, grid[(x, y)]))


def main(argv):
    target = int(argv[1])
    fill(grid, target)


if __name__ == '__main__':
    main(sys.argv)
