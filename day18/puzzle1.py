#!/usr/bin/env python

import sys

TRAPS = [(True, True, False),
         (False, True, True),
         (True, False, False),
         (False, False, True)]

def read_row(infile):
    with open(infile, 'rb') as f:
        data = f.read()
    return data.strip()

def tile_is_trap(room, row, i):
    if i < 0 or i >= len(room[0]):
        return False
    else:
        return room[row][i] == '^'

def is_trap(room, row, i):
    prev_traps = (tile_is_trap(room, row - 1, i - 1),
                  tile_is_trap(room, row - 1, i),
                  tile_is_trap(room, row - 1, i + 1))
    return prev_traps in TRAPS

def make_row(row, room):
    prev_row = row - 1
    tiles = len(room[prev_row])
    print 'Generating %d tiles' % (tiles)
    new_row = ['.'] * tiles
    for i in range(tiles):
        if is_trap(room, row, i):
            new_row[i] = '^'
    return ''.join(new_row)

def main(argv=None):
    if not argv:
        argv = sys.argv
    infile = argv[1]
    room = []
    room.append(read_row(infile))
    row = 1
    while row < int(argv[2]):
        room.append(make_row(row, room))
        row += 1
    safe_tiles = 0
    for row in room:
        safe_tiles += row.count('.')
    print 'Counted %d safe tiles' % (safe_tiles)

if __name__ == '__main__':
    main()
