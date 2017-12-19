#!/usr/bin/env python3

# http://adventofcode.com/2017/day/17

import sys

STEP = 3
STEP = 356


def insert(buf_len, pos, item):
    new_pos = pos + STEP
    new_pos %= buf_len
    new_pos += 1
    return new_pos


def main(argv):
    # Starting state
    buf_len = 1
    pos = 0
    for item in range(50000000):
        pos = insert(buf_len, pos, item + 1)
        buf_len += 1
        if pos == 1:
            print('Now at position 1: %d' % (item + 1))
        # else:
        #     print('.')


if __name__ == '__main__':
    main(sys.argv)
