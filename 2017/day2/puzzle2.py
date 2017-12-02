#!/usr/bin/env python3

# http://adventofcode.com/2017/day/2

import sys


def find_quotient(nums):
    count = len(nums)
    for x in range(0, count):
        a = nums[x]
        for y in range(x + 1, count):
            b = nums[y]
            # print('[%d] = %d; [%d] = %d' % (n, a, x, b))
            if a % b == 0:
                return a / b
            elif b % a == 0:
                return b / a
    raise Exception('No divisors found')


def compute_checksum(datafile):
    """Checksum is the sum of the quotient between the
    two values on each line where one is evenly divisible by
    the other.
    """
    checksum = 0
    with open(datafile, 'rb') as f:
        for line in f:
            # Remove trailing newline, split on tabs
            nums = [int(x) for x in line.strip(b'\n').split(b'\t')]
            checksum += find_quotient(nums)
    return checksum


def main(argv):
    datafile = argv[1]
    checksum = compute_checksum(datafile)
    print('Checksum = %d' % (checksum))


if __name__ == '__main__':
    main(sys.argv)
