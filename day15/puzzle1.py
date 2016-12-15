#!/usr/bin/env python

import re
import sys

# Disc #1 has 13 positions; at time=0, it is at position 10.
prog = re.compile(r'Disc #(\d+) has (\d+) positions; at time=(\d+), it is at position (\d+)\.')

def load_discs(filename):
    discs = []
    with open(filename, 'rb') as f:
        for line in f:
            m = prog.match(line)
            if m:
                discs.append([int(x) for x in m.groups()])
            else:
                print 'No match', line
    return discs

def find_start_time(disc, positions, time, pos):
    """What button press time step would match this disc in
    the open position?
    """
    # Assume time is zero for now
    return positions - ((disc + pos) % positions)

def disc_open(ts, disc, positions, time, pos):
    return (ts + disc + pos) % positions == 0

def all_open(ts, discs):
    for d in discs:
        if not disc_open(ts, *d):
            return False
    return True

def main(argv=None):
    if not argv:
        argv = sys.argv
    discs = load_discs(argv[1])
    max_positions = 0
    st = 0
    for d in discs:
        if d[1] > max_positions:
            max_positions = d[1]
            st = find_start_time(*d)
    print 'most positions =', max_positions, 'st =', st
    ts = st
    while True:
        if all_open(ts, discs):
            print 'All discs open with button press at ', ts
            break
        ts += max_positions

if __name__ == '__main__':
    main()
