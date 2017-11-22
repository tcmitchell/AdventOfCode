#!/usr/bin/env python

import sys

class World(object):

    def __init__(self, width, height, magic_number):
        self.width = width
        self.height = height
        self.magic_number = magic_number
        self.world = []
        for y in range(height):
            self.world.append(['.'] * width)
        self.make_walls(self.magic_number)

    def __str__(self):
        result = ''
        for y in range(self.height):
            result += ''.join(self.world[y])
            result += '\n'
        return result

    def is_wall(self, x, y):
        return True

    def make_walls(self, magic_number):
        for y in range(self.height):
            for x in range(self.width):
                val = x*x + 3*x + 2*x*y + y + y*y
                val += magic_number
                if bin(val).count('1') % 2 == 1:
                    # Odd, so wall
                    self.world[y][x] = '#'

def is_wall(x, y, magic_number):
    val = x*x + 3*x + 2*x*y + y + y*y + magic_number
    return bin(val).count('1') % 2 == 1

def legal_move(x, y, magic_number):
    return x > 0 and y > 0 and not is_wall(x, y, magic_number)

def main(argv=None):
    if not argv:
        argv = sys.argv
    magic_number = int(argv[1])
    visited = []
    to_explore = [(1, 1, 0)]
    while to_explore:
        (x, y, gen) = to_explore.pop(0)
        print (x, y, gen)
        visited.append((x, y))
        for (next_x, next_y) in [(x, y-1), (x, y+1), (x+1, y), (x-1, y)]:
            if (next_x, next_y) in visited:
                continue
            if not legal_move(next_x, next_y, magic_number):
                visited.append((next_x, next_y))
                continue
            if next_x == 31 and next_y == 39:
                print 'Finished at generation', gen+1
                return gen+1
            to_explore.append((next_x, next_y, gen+1))

# 38 is too low
# 68 is too low

if __name__ == '__main__':
    main()
