#!/usr/bin/env python

import re
import sys

def decompress(indata):
    prog = re.compile(r'\((\d+)x(\d+)\)')
    whitespace = re.compile(r'\s')
    outdata = ''
    while indata:
        m = prog.match(indata)
        if m:
            count = int(m.group(1))
            times = int(m.group(2))
            indata = indata[len(m.group(0)):]
            for n in range(times):
                outdata += indata[0:count]
            indata = indata[count:]
        elif whitespace.match(indata[0]):
            indata = indata[1:]
        else:
            outdata += indata[0]
            indata = indata[1:]
    return outdata

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
    print len(decompressed_data)

if __name__ == '__main__':
    main()
