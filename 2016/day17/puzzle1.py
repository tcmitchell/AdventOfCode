#!/usr/bin/env python

import md5
import sys

def legal_move(x, y, passcode, path):
    return x >= 0 and x < 5 and y >= 0 and y < 5

def next_moves(x, y, passcode, path):
    # Returns a list of the possible next moves from here
    path_hash = md5.md5(passcode + path).hexdigest()
    (u, d, l, r) = [l > 'a' for l in path_hash[0:4]]
    moves = []
    if u and legal_move(x, y-1, passcode, path + 'U'):
        moves.append((x, y-1, passcode, path + 'U'))
    if d and legal_move(x, y+1, passcode, path + 'D'):
        moves.append((x, y+1, passcode, path + 'D'))
    if l and legal_move(x-1, y, passcode, path + 'L'):
        moves.append((x-1, y, passcode, path + 'L'))
    if r and legal_move(x+1, y, passcode, path + 'R'):
        moves.append((x+1, y, passcode, path + 'R'))
    return moves

def main(argv=None):
    if not argv:
        argv = sys.argv
    passcode = argv[1]
    frontier = [(1, 1, passcode, '')]
    while frontier:
        (x, y, passcode, path) = frontier.pop(0)
        print (x, y, passcode, path)
        moves = next_moves(x, y, passcode, path)
        for (next_x, next_y, next_passcode, next_path) in moves:
            if next_x == 4 and next_y == 4:
                print 'Finished with path', next_path
                return
            frontier.append((next_x, next_y, next_passcode, next_path))

if __name__ == '__main__':
    main()
