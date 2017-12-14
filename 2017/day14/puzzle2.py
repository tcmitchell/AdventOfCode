#!/usr/bin/env python3

# http://adventofcode.com/2017/day/14

import sys

import knothash

GRID_SIZE = 128


# Data is all on one line
def load_input(datafile):
    with open(datafile, 'rb') as f:
        return f.read().rstrip()


def to_bin(kh):
    # knothashes are hex
    scale = 16
    # each hex character in a knothash represents 4 bits
    num_of_bits = len(kh) * 4
    return bin(int(kh, scale))[2:].zfill(num_of_bits)


def make_grid(key_string):
    grid = []
    for i in range(GRID_SIZE):
        key = key_string + b'-' + bytes(str(i), 'utf-8')
        aoc_hash = knothash.knothash(key)
        # print('Hash for %r: %r' % (key, aoc_hash))
        # print('\t%r' % (to_bin(aoc_hash)))
        aoc_bin = to_bin(aoc_hash)
        grid.append(list(aoc_bin.replace('1', '#').replace('0', '.')))
    return grid


def block_in_grid(grid, pos):
    (r, c) = pos
    return r >= 0 and r < GRID_SIZE and c >= 0 and c < GRID_SIZE


def block_is_used(grid, pos):
    (r, c) = pos
    return block_in_grid(grid, pos) and grid[r][c] == '#'


def find_used_block(grid):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if block_is_used(grid, (r, c)):
                return(r, c)
    return None


def find_used_neighbors(grid, pos):
    (r, c) = pos
    neighbors = [(r, c - 1), (r, c + 1), (r - 1, c), (r + 1, c)]
    # print('[%d, %d] has neighbors %r' % (r, c, neighbors))
    result = [n for n in neighbors if block_is_used(grid, n)]
    # print('[%d, %d] has used neighbors %r' % (r, c, result))
    return result


def mark_block(grid, pos, region_id):
    (r, c) = pos
    grid[r][c] = region_id


def mark_region(grid, region_id):
    pos = find_used_block(grid)
    if pos is None:
        return False
    neighbors = [pos]
    # print('Neighbors = %r' % (neighbors))
    while neighbors:
        new_neighbors = []
        for n in neighbors:
            mark_block(grid, n, region_id)
            new_neighbors.extend(find_used_neighbors(grid, n))
        neighbors = new_neighbors
        # print('Neighbors = %r' % (neighbors))
    return True


def mark_regions(grid):
    region_id = 0
    while mark_region(grid, region_id + 1):
        region_id += 1
    return region_id


def main(argv):
    # knothash.test()
    datafile = argv[1]
    key_string = load_input(datafile)
    grid = make_grid(key_string)
    regions = mark_regions(grid)
    for i in range(8):
        for j in range(8):
            print(grid[i][j], end='')
        print('')
    print('There are %d regions' % (regions))


if __name__ == '__main__':
    main(sys.argv)
