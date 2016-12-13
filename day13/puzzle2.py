#!/usr/bin/env python

import sys

def is_wall(x, y, magic_number):
    val = x*x + 3*x + 2*x*y + y + y*y + magic_number
    return bin(val).count('1') % 2 == 1

def legal_move(x, y, magic_number):
    return x >= 0 and y >= 0 and not is_wall(x, y, magic_number)

def main(argv=None):
    if not argv:
        argv = sys.argv
    magic_number = int(argv[1])
    visited = set()
    visited50 = set()
    frontier = [(1, 1, 0)]
    while frontier:
        (x, y, gen) = frontier.pop(0)
        print (x, y, gen)
        visited.add((x, y))
        if gen < 51:
            visited50.add((x, y))
        for (next_x, next_y) in [(x, y-1), (x, y+1), (x+1, y), (x-1, y)]:
            if (next_x, next_y) in visited:
                continue
            if not legal_move(next_x, next_y, magic_number):
                continue
            if next_x == 31 and next_y == 39:
                print 'Finished at generation', gen+1
                print 'Visited in 50:', len(visited50)
                return gen+1
            frontier.append((next_x, next_y, gen+1))

# 263 is too high (gen 50) - duplicates in visited, illegal moves in visited
# 261 is too high (gen 49) - duplicates in visited, illegal moves in visited
# 118 is too low (don't put illegal moves in visited set)
# 119 is too low (tried to generation 51) - wasn't exploring zeroes
# 135 is correct: is_legal wasn't allowing zero coordinates, which are
#                 legal. Changed from x > 0 to x >= 0

if __name__ == '__main__':
    main()
