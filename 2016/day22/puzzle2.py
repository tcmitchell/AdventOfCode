#!/usr/bin/env python

import copy
import pprint
import re
import sys

node_prog = re.compile(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s*\d+T')
#node_prog = re.compile(r'(/dev/grid\S*)')

SIZE = 0
USED = 1

def load_nodes(infile):
    X = 0
    Y = 1
    nodes = []
    with open(infile, 'rb') as f:
        for line in f:
            match = node_prog.match(line)
            if match:
                nodes.append([int(x) for x in match.groups()])
    max_x = max([n[X] for n in nodes])
    max_y = max([n[Y] for n in nodes])
    grid = []
    # Build the grid full of None
    grid.extend([[None]*(max_y+1) for x in range(max_x + 1)])
    for n in nodes:
        grid[n[X]][n[Y]] = [n[2], n[3]]
        # if n[X] == 17 and n[Y] == 22:
        #     print (n[2], n[3])
    return grid

# For each move, record the location of the target data
# and record the empty cell (instead of finding it each time)

def find_empty_node(grid):
    """There should be one and only one empty node. Find it
    and return its location as a tuple."""
    for x in range(len(grid)):
        row = grid[x]
        for y in range(len(row)):
            if row[y][USED] == 0:
                return (x, y)
            # else:
            #     print x, y, row[y][USED]
    raise Exception('No empty node found')

class Move(object):

    def __init__(self, grid, empty, target, generation):
        self.grid = grid
        self.empty = empty
        self.target = target
        self.generation = generation

    def done(self):
        return self.target == (0, 0)

    def next_moves(self):
        empty_x, empty_y = self.empty
        curr = self.grid[empty_x][empty_y]
        moves = []
        for empty in [(empty_x - 1, empty_y), (empty_x + 1, empty_y),
                      (empty_x, empty_y - 1), (empty_x, empty_y + 1)]:
            next_x, next_y = empty
            if (next_x < 0 or next_x >= len(self.grid) or
                next_y < 0 or next_y >= len(self.grid[0])):
                    print (next_x, next_y), 'out of bounds'
                    continue
            # print 'next_moves next_x', next_x, 'next_y', next_y
            # print 'next_moves len_x', len(self.grid), 'len_y', len(self.grid[0])
            next = self.grid[next_x][next_y]
            # Can the empty node hold the next node's data?
            if curr[SIZE] < next[USED]:
                print 'not enough capacity from ', (empty_x, empty_y), 'to', (next_x, next_y)
                continue
            target = self.target
            if (empty == self.target):
                target = self.empty
                print 'target moved to ', target
            next_grid = copy.deepcopy(self.grid)
            next_grid[empty_x][empty_y][USED] = next[USED]
            next_grid[next_x][next_y][USED] = 0
            moves.append(Move(next_grid, empty, target, self.generation + 1))
        return moves

def old_main(argv=None):
    if argv is None:
        argv = sys.argv
    infile = argv[1]
    grid = load_nodes(infile)
    # pprint.pprint(grid)
    empty_node = find_empty_node(grid)
    print empty_node
    frontier = [Move(grid, empty_node, (len(grid) - 1, 0), 0)]
    visited = []
    while frontier:
        move = frontier.pop(0)
        # print 'Exploring empty', move.empty, '; target', move.target, 'gen', move.generation
        # pprint.pprint(move.grid)
        # print '-----------------------'
        print 'Exploring a move in generation ', move.generation
        if (move.grid, move.empty, move.target) in visited:
            print 'Already visited'
            continue
        else:
            visited.append((move.grid, move.empty, move.target))
        next_moves = move.next_moves()
        for nm in next_moves:
            if nm.done():
                print nm.generation
                return nm.generation
            frontier.append(nm)
    # print visited

def main(argv=None):
    if argv is None:
        argv = sys.argv
    infile = argv[1]
    grid = load_nodes(infile)
    for y in range(len(grid[0])):
        for x in range(len(grid)):
            if (x == 35 and y == 0):
                sys.stdout.write('G')
            elif grid[x][y][USED] > 100:
                sys.stdout.write('-')
            elif grid[x][y][USED] == 0:
                sys.stdout.write('E')                
            else:
                sys.stdout.write('.')
        print

if __name__ == '__main__':
    main()
