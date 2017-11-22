#!/usr/bin/env python

import re
import sys

class Screen(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = []
        for y in range(self.height):
            self.pixels.append([' ']*self.width)

    def rect(self, width, height):
        for x in range(width):
            for y in range(height):
                self.pixels[y][x] = '#'

    def rotate_row(self, row, count):
        old_row = self.pixels[row]
        new_row = old_row[-count:]
        new_row.extend(old_row[:-count])
        self.pixels[row] = new_row

    def rotate_column_1(self, column):
        last = self.pixels[self.height - 1][column]
        for i in reversed(range(1, self.height)):
            self.pixels[i][column] = self.pixels[i - 1][column]
        self.pixels[0][column] = last

    def rotate_column(self, column, count):
        for i in range(count):
            self.rotate_column_1(column)

    def __str__(self):
        result = ''
        for y in range(self.height):
            result += ''.join(self.pixels[y])
            result += '\n'
        return result

    def count_on_pixels(self):
        count = 0
        for y in range(self.height):
            count += self.pixels[y].count('#')
        return count

def do_rect(screen, w, h):
    w = int(w)
    h = int(h)
    print 'do_rect(%d, %d)' % (w, h)
    screen.rect(w, h)

def do_rotate_row(screen, r, num):
    r = int(r)
    num = int(num)
    print 'do_rotate_row(%d, %d)' % (r, num)
    screen.rotate_row(r, num)

def do_rotate_column(screen, c, num):
    c = int(c)
    num = int(num)
    print 'do_rotate_column(%d, %d)' % (c, num)
    screen.rotate_column(c, num)

def get_command_parsers():
    return [(re.compile(r'rect (\d+)x(\d+)'), do_rect),
            (re.compile(r'rotate row y=(\d+) by (\d+)'), do_rotate_row),
            (re.compile(r'rotate column x=(\d+) by (\d+)'), do_rotate_column)]

def do_command(screen, cmd, parsers):
    for (regex, func) in parsers:
        m = regex.match(cmd)
        if m:
            return func(screen, m.group(1), m.group(2))
    raise Exception("Unknown command: " + cmd)

def load_commands(screen, datafile):
    parsers = get_command_parsers()
    with open(datafile, 'rb') as f:
        for line in f:
            line = line.strip()
            do_command(screen, line, parsers)
            print screen
            print

def main(argv):
    datafile = argv[1]
    screen = Screen(50, 6)
    print screen
    load_commands(screen, datafile)
    print 'On pixels: ', screen.count_on_pixels()

if __name__ == '__main__':
    main(sys.argv)
