#!/usr/bin/env python

import sys

class Triangle(object):

    def __init__(self, line):
        (a, b, c) = self.parse_line(line)
        self.a = a
        self.b = b
        self.c = c

    def parse_line(self, line):
        int_vals = [int(x) for x in line.split()]
        return tuple(int_vals)

    def is_possible(self):
        return ((self.a + self.b > self.c) and
                (self.b + self.c > self.a) and
                (self.a + self.c > self.b))


def parse_input(fname):
    triangles = []
    with open(fname, 'rb') as f:
        for line in f:
            triangles.append(Triangle(line))
    return triangles

def main(argv):
    datafile = argv[1]
    print datafile
    data = parse_input(datafile)
    num_triangles = 0
    possible_triangles = 0
    for triangle in data:
        num_triangles += 1
        if triangle.is_possible():
            possible_triangles += 1
    msg = 'There were %d possible triangles in %d triangles.'
    print msg % (possible_triangles, num_triangles)

if __name__ == '__main__':
    main(sys.argv)
