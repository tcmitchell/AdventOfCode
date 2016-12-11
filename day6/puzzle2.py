#!/usr/bin/env python

import sys
import collections

class Decoder(object):

    def __init__(self):
        self.counters = None

    def init_counters(self, row):
        self.counters = [collections.Counter() for x in range(len(row))]

    def load_row(self, row):
        if not self.counters:
            self.init_counters(row)
        for x in range(len(row)):
            self.counters[x].update(row[x])

    def load_data(self, datafile):
        with open(datafile, 'rb') as f:
            for line in f:
                self.load_row(line.strip())

    def message(self):
        msg = []
        for c in self.counters:
            freq = c.most_common()
            freq.reverse()
            msg.append(freq[0][0])
        return ''.join(msg)

def main(argv):
    datafile = argv[1]
    decoder = Decoder()
    decoder.load_data(datafile)
    print 'The message is', decoder.message()

if __name__ == '__main__':
    main(sys.argv)
