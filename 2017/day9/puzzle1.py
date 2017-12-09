#!/usr/bin/env python3

# http://adventofcode.com/2017/day/9

import sys


# Data is all on one line
def load_input(datafile):
    with open(datafile, 'rb') as f:
        return f.read().decode('utf-8').rstrip()


def filter_garbage(in_data):
    out = []
    in_size = len(in_data)
    in_ptr = 0
    in_garbage = False
    while in_ptr < in_size:
        in_char = in_data[in_ptr]
        if in_garbage:
            if in_char == '!':
                in_ptr += 1
            elif in_char == '>':
                in_garbage = False
            else:
                pass
        else:
            if in_char == '<':
                in_garbage = True
            else:
                out.append(in_data[in_ptr])
        in_ptr += 1
    return ''.join(out)


def main(argv):
    datafile = argv[1]
    raw_data = load_input(datafile)
    fdata = filter_garbage(raw_data)
    print(fdata)


if __name__ == '__main__':
    main(sys.argv)
