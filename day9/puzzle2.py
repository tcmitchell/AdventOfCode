#!/usr/bin/env python

import re
import sys

marker_prog = re.compile(r'\((\d+)x(\d+)\)')

def decompress(indata):
    whitespace = re.compile(r'\s')
    data_length = 0
    while indata:
        m = marker_prog.match(indata)
        if m:
            count = int(m.group(1))
            times = int(m.group(2))
            indata = indata[len(m.group(0)):]
            data_length += times * decompress(indata[0:count])
            indata = indata[count:]
        elif whitespace.match(indata[0]):
            indata = indata[1:]
        else:
            data_length += 1
            indata = indata[1:]
    return data_length

def load_data(datafile):
    with open(datafile, 'rb') as f:
        return f.read()

def main(argv=None):
    if not argv:
        argv = sys.argv
    datafile = argv[1]
    compressed_data = load_data(datafile)
    decompressed_data = decompress(compressed_data)
    print decompressed_data
    # print len(decompressed_data)

if __name__ == '__main__':
    main()
