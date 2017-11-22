#!/usr/bin/env python

import sys
import re
import collections

class Room(object):

    def __init__(self, name, sector_id, checksum):
        self.name = name
        self.sector_id = sector_id
        self.checksum = checksum

    @staticmethod
    def cmp_freq(x, y):
        """Compares two frequency tuples"""
        # print 'compare:', x, y
        (xl, xn) = x
        (yl, yn) = y
        result = cmp(yn, xn)
        if result == 0:
            result = cmp(xl, yl)
        # print 'cmp_freq result =', result
        return result

    def compute_checksum(self):
        # Determine frequency of each letter in name
        # Checksum is the top 5 letters, ordered by
        # frequency, and alphabetical within frequency
        letters = collections.Counter(self.name)
        letters.pop('-', None)
        #sorted(list(set(letters.values())), reverse=True)
        letters = sorted(tuple(letters.items()), Room.cmp_freq)
        # print 'Sorted:', letters
        long_checksum = ''.join([l for (l, n) in letters])
        # print 'Long Checksum:', long_checksum
        return long_checksum[0:5]

    def is_real(self):
        return self.checksum == self.compute_checksum()

def parse_line(string):
    pattern = r'(.*)-(\d+)\[(.*)\]$'
    result = re.match(pattern, string)
    return Room(result.group(1), result.group(2), result.group(3))

def load_rooms(fname):
    with open(fname, 'rb') as f:
        return [parse_line(line) for line in f]

def main(argv):
    datafile = argv[1]
    rooms = load_rooms(datafile)
    sector_sum = 0
    for room in rooms:
        if room.is_real():
            sector_sum += int(room.sector_id)
    print 'Sum of sectors:', sector_sum

if __name__ == '__main__':
    main(sys.argv)
