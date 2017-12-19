#!/usr/bin/env python3

# http://adventofcode.com/2017/day/17

import sys

STEP = 3
STEP = 356


def insert(buf, pos, item):
    new_pos = pos + STEP
    new_pos %= len(buf)
    new_pos += 1
    buf.insert(new_pos, item)
    return new_pos


def main(argv):
    # Starting state
    buf = [0]
    pos = 0
    print(buf)
    for item in range(2017):
        pos = insert(buf, pos, item + 1)
        # print(pos, buf)
    print('The number after 2017 is %d' % (buf[buf.index(2017) + 1]))


if __name__ == '__main__':
    main(sys.argv)
