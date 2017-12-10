#!/usr/bin/env python3

# http://adventofcode.com/2017/day/9

import sys

DATA_SIZE = 5
DATA_SIZE = 256


# Data is all on one line
def load_input(datafile):
    with open(datafile, 'rb') as f:
        return [int(x) for x in f.read().decode('utf-8').rstrip().split(',')]


def insert(data, pos, length, sub_data):
    data_len = len(data)
    if pos + length > data_len:
        # insert to end and then from beginning of data
        part1_size = data_len - pos
        part2_size = length - part1_size
        data[pos:] = sub_data[0:part1_size]
        data[0:part2_size] = sub_data[part1_size:]
    else:
        data[pos:pos + length] = sub_data


def extract(data, pos, length):
    data_len = len(data)
    if pos + length > data_len:
        # assemble the extract from end and beginning of data
        result = data[pos:]
        length -= data_len - pos
        result.extend(data[0:length])
        return result
    else:
        return data[pos:pos + length]


def twist(data, pos, length):
    if length == 1:
        return
    extracted = extract(data, pos, length)
    print('extract = %r' % (extracted))
    extracted.reverse()
    print('reversed = %r' % (extracted))
    insert(data, pos, length, extracted)


def main(argv):
    datafile = argv[1]
    lengths = load_input(datafile)
    data = list(range(DATA_SIZE))
    skip_size = 0
    pos = 0
    for length in lengths:
        twist(data, pos, length)
        pos += length + skip_size
        pos %= DATA_SIZE
        skip_size += 1
        print('data = %r; ptr = %d; skip_size = %d' % (data, pos, skip_size))
    print('check hash: %d * %d = %d' % (data[0], data[1], data[0] * data[1]))


if __name__ == '__main__':
    main(sys.argv)
