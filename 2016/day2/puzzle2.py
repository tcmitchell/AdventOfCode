#!/usr/bin/env python

import sys

class KeyPad(object):

    board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D']
    up =    [0, 1, 0, 3, 4, 1, 2, 3, 8, 5, 6, 7, 10]
    down =  [2, 5, 6, 7, 4, 9, 10, 11, 8, 9, 12, 11, 12]
    left =  [0, 1, 1, 2, 4, 4, 5, 6, 7, 9, 9, 10, 12]
    right = [0, 2, 3, 3, 5, 6, 7, 8, 8, 10, 11, 11, 12]

    def __init__(self):
        # Start at the middle button, '5'
        self._pos = 4

    def move(self, direction):
        if direction == 'U':
            self._pos = KeyPad.up[self._pos]
        elif direction == 'D':
            self._pos = KeyPad.down[self._pos]
        elif direction == 'L':
            self._pos = KeyPad.left[self._pos]
        elif direction == 'R':
            self._pos = KeyPad.right[self._pos]

    def getNumber(self):
        return KeyPad.board[self._pos]

def parse_input(fname):
    with open(fname, 'rb') as f:
        return [l.strip() for l in f]

def main(argv):
    datafile = argv[1]
    print datafile
    data = parse_input(datafile)
    for x in data:
        print x
    keypad = KeyPad()
    print 'Starting at', keypad.getNumber()
    for line in data:
        for direction in line:
            keypad.move(direction)
        print 'Next number:', keypad.getNumber()

if __name__ == '__main__':
    main(sys.argv)
