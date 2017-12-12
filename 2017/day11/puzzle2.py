#!/usr/bin/env python3

# http://adventofcode.com/2017/day/11

# Helpful resource on hexagonal grids:
#
#   https://www.redblobgames.com/grids/hexagons/
#

import sys

TEST_DATA = [(b'ne,ne,ne', 3),
             (b'ne,ne,sw,sw', 0),
             (b'ne,ne,s,s', 2),
             (b'se,sw,se,sw,sw', 3)
             ]


def load_input(datafile):
    with open(datafile, 'rb') as f:
        return f.read().strip()


def axial_distance(a_q, a_r, b_q, b_r):
    return (abs(a_q - b_q)
            + abs(a_q + a_r - b_q - b_r)
            + abs(a_r - b_r)) / 2


def travel(q, r, step):
    # q is column, r is row
    if step == b'ne':
        q += 1
        r -= 1
    elif step == b'se':
        q += 1
    elif step == b's':
        r += 1
    elif step == b'sw':
        q -= 1
        r += 1
    elif step == b'nw':
        q -= 1
    elif step == b'n':
        r -= 1
    else:
        raise Exception('Unknown travel step %r' % (step))
    return (q, r)


def compute_distance(steps):
    q = 0
    r = 0
    max_dist = 0
    for step in steps:
        (q, r) = travel(q, r, step)
        dist = axial_distance(0, 0, q, r)
        if dist > max_dist:
            max_dist = dist
    return (axial_distance(0, 0, q, r), max_dist)


def run_tests():
    for (data, expected_result) in TEST_DATA:
        steps = data.split(b',')
        result = compute_distance(steps)
        if result == expected_result:
            print('Test %r: PASS' % (data))
        else:
            print('Test %r: FAIL (expected %d, got %d)' %
                  (data, expected_result, result))


def main(argv):
    if len(argv) == 1:
        run_tests()
        return 0

    datafile = argv[1]
    data = load_input(datafile)
    steps = data.split(b',')
    (cur_dist, max_dist) = compute_distance(steps)
    print('Current Distance = %d' % (cur_dist))
    print('Max Distance = %d' % (max_dist))


if __name__ == '__main__':
    main(sys.argv)
