#!/usr/bin/env python

import sys

def load_data(filename):
    with open(filename, 'rb') as f:
        return f.read()

def main(argv=None):
    if not argv:
        argv = sys.argv
    instructions = load_data(argv[1])
    print len(instructions), 'instructions'
    floor = 0
    for i in instructions:
        if i == '(':
            floor += 1
        elif i == ')':
            floor -= 1
    print floor

if __name__ == '__main__':
    main()
