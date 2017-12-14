#!/usr/bin/env python3

# http://adventofcode.com/2017/day/10

import functools
import operator
import sys

DATA_SIZE = 256


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
    # print('extract = %r' % (extracted))
    extracted.reverse()
    # print('reversed = %r' % (extracted))
    insert(data, pos, length, extracted)


def hash_to_hex(data):
    dense_hash = []
    for i in range(16):
        start = i * 16
        end = start + 16
        # print('data 16: %r' % (data[start:end]))
        dense_hash.append(functools.reduce(operator.xor, data[start:end]))
    # print('Dense hash: %r' % (dense_hash))
    hex_list = [format(dh, '02x') for dh in dense_hash]
    return ''.join(hex_list)


def bytes_to_lengths(bites):
    result = [b for b in bites]
    result.extend([17, 31, 73, 47, 23])
    return result


def knothash(bites):
    lengths = bytes_to_lengths(bites)
    data = list(range(DATA_SIZE))
    skip_size = 0
    pos = 0
    for kh_round in range(64):
        for length in lengths:
            twist(data, pos, length)
            pos += length + skip_size
            pos %= DATA_SIZE
            skip_size += 1
        # print('data = %r; ptr = %d; skip_size = %d' % (data, pos, skip_size))
    return hash_to_hex(data)


def run_test(bites, expected):
    result = knothash(bites)
    print('Result = %r' % (result))
    if result == expected:
        print('Test %r: PASS' % (bites))
    else:
        print('Test %r: FAIL' % (bites))


test_data = [(b'', 'a2582a3a0e66e6e86e3812dcb672a272'),
             (b'AoC 2017', '33efeb34ea91902bb2f59c9920caa6cd'),
             (b'1,2,3', '3efbe78a8d82f29979031a4aa0b16a9d'),
             (b'1,2,4', '63960835bcdc130f0b66d7ff4f6a5a8e')
             ]


def test():
    for (bites, expected) in test_data:
        run_test(bites, expected)
