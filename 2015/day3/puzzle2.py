#!/usr/bin/env python

import sys
from collections import defaultdict


def load_data(filename):
    with open(filename, 'rb') as f:
        return f.read()

def next_loc(loc, i):
    (x, y) = loc
    if i == '^':
        y += 1
    elif i == 'v':
        y -= 1
    elif i == '>':
        x += 1
    elif i == '<':
        x -= 1
    return (x, y)

def main(argv=None):
    if not argv:
        argv = sys.argv
    instructions = load_data(argv[1])
    visited = defaultdict(lambda:0)
    santa = (0, 0)
    robot = (0, 0)
    visited[santa] += 1
    visited[robot] += 1
    for i in range(len(instructions)):
        inst = instructions[i]
        if inst not in '^v<>':
            continue
        if i % 2 == 0:
            robot = next_loc(robot, inst)
            visited[robot] += 1
        else:
            santa = next_loc(santa, inst)
            visited[santa] += 1
    print len(visited)

if __name__ == '__main__':
    main()
