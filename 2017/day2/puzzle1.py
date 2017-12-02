#!/usr/bin/env python3

# http://adventofcode.com/2017/day/2

import sys


def compute_checksum(datafile):
    """Checksum is the sum of the differences between the
    minimum and maximum value on each line of a tab delimited
    data file.
    """
    checksum = 0
    with open(datafile, 'rb') as f:
        for line in f:
            # Remove trailing newline, split on tabs
            nums = [int(x) for x in line.strip(b'\n').split(b'\t')]
            checksum += max(nums) - min(nums)
    return checksum


def main(argv):
    datafile = argv[1]
    checksum = compute_checksum(datafile)
    print('Checksum = %d' % (checksum))


if __name__ == '__main__':
    main(sys.argv)
