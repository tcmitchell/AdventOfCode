#!/usr/bin/env python3

# http://adventofcode.com/2017/day/15

import sys

GEN_A_FACTOR = 16807
GEN_B_FACTOR = 48271
GEN_A_CRITERIA = 4
GEN_B_CRITERIA = 8
GEN_DIVISOR = 2147483647

# Test seeds
GEN_A_SEED = 65
GEN_B_SEED = 8921

# Production seeds
GEN_A_SEED = 703
GEN_B_SEED = 516


class Generator():

    def __init__(self, factor, seed, criteria):
        self.factor = factor
        self.previous = seed
        self.criteria = criteria
        self.divisor = GEN_DIVISOR

    def next_value(self):
        while True:
            result = self.previous * self.factor % self.divisor
            self.previous = result
            if result % self.criteria == 0:
                return result


def low16bits(val):
    return bin(val)[-16:]


def main(argv):
    genA = Generator(GEN_A_FACTOR, GEN_A_SEED, GEN_A_CRITERIA)
    genB = Generator(GEN_B_FACTOR, GEN_B_SEED, GEN_B_CRITERIA)
    score = 0
    for i in range(5000000):
        a_val = genA.next_value()
        b_val = genB.next_value()
        # print('Next: %r\t%r' % (a_val, b_val))
        if low16bits(a_val) == low16bits(b_val):
            score += 1
    print('Score: %r' % (score))


if __name__ == '__main__':
    main(sys.argv)
