#!/usr/bin/env python3

# http://adventofcode.com/2017/day/13

import sys


def parse_line(input_line):
    return tuple([int(x) for x in input_line.split(b':')])


def load_input(datafile):
    with open(datafile, 'rb') as f:
        return [parse_line(l) for l in f.readlines()]


def main(argv):
    datafile = argv[1]
    max_delay = int(argv[2])
    data = load_input(datafile)
    print(data)
    delay = 0
    while delay < max_delay:
        # print('Checking delay %d' % (delay))
        detected = False
        for (d, r) in data:
            # Compute number of positions for scanner
            p = max(r, r + r - 2)
            # print('Depth %d has %d positions' % (d, p))
            # print('Depth %d scanner is at position %d' % (d, (d + delay) % p))
            if (d + delay) % p == 0:
                detected = True
                break
        print('Delay %d has detected = %r' % (delay, detected))
        if not detected:
            break
        else:
            delay += 1
    print('Delay for no detection = %d' % (delay))


if __name__ == '__main__':
    main(sys.argv)
