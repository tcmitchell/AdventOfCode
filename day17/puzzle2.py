#!/usr/bin/env python

import md5
import sys

def legal_move(x, y, passcode, path):
    return x >= 0 and x < 4 and y >= 0 and y < 4

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
    frontier = [(0, 0, passcode, '')]
    longest = 0
    while frontier:
        (x, y, passcode, path) = frontier.pop()
        # print (x, y, passcode, path)
        if x == 3 and y == 3:
            path_len = len(path)
            if longest < path_len:
                longest = path_len
                print 'longest so far is ', longest
            continue
        moves = next_moves(x, y, passcode, path)
        frontier.extend(moves)
    print 'Longest path is ', longest

if __name__ == '__main__':
    main()
