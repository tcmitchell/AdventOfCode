#!/usr/bin/env python3

# http://adventofcode.com/2017/day/15

import sys

GEN_A_FACTOR = 16807
GEN_B_FACTOR = 48271
GEN_DIVISOR = 2147483647

GEN_A_TEST_SEED = 65
GEN_B_TEST_SEED = 8921

GEN_A_SEED = 703
GEN_B_SEED = 516


class Generator():

    def __init__(self, factor, seed):
        self.factor = factor
        self.previous = seed
        self.divisor = GEN_DIVISOR

    def next_value(self):
        result = self.previous * self.factor % self.divisor
        self.previous = result
        return result


def low16bits(val):
    return bin(val)[-16:]


def main(argv):
    genA = Generator(GEN_A_FACTOR, GEN_A_SEED)
    genB = Generator(GEN_B_FACTOR, GEN_B_SEED)
    score = 0
    for i in range(40000000):
        a_val = genA.next_value()
        b_val = genB.next_value()
        if low16bits(a_val) == low16bits(b_val):
            score += 1
    print('Score: %r' % (score))


if __name__ == '__main__':
    main(sys.argv)
