#!/usr/bin/env python3

# http://adventofcode.com/2017/day/19

import sys


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Position(%d, %d)' % (self.x, self.y)


class Packet:
    def __init__(self):
        self.letters = []

    def add_letter(self, letter):
        self.letters.append(letter)


# Data is a big grid
def load_input(datafile):
    with open(datafile, 'rb') as f:
        return [line.rstrip(b'\n').decode('utf-8') for line in f]


def find_start_pos(diagram):
    # Puzzle starts by heading south from the top line (row 0)
    # Find the one '|' on the first line and return the position
    y = 0
    x = diagram[y].index('|')
    return Position(x, y)


def stop_packet(grid, packet, pos):
    print('Stopping. Letters encountered: %s' % (''.join(packet.letters)))
    sys.exit()


def move_north(grid, packet, pos):
    pos.y -= 1
    next_square = grid[pos.y][pos.x]
    if next_square == '|' or next_square == '-':
        # Continue south
        return move_north
    elif next_square == '+':
        # Change direction
        if grid[pos.y][pos.x - 1] == ' ':
            # West is blank, move East
            return move_east
        else:
            return move_west
    elif next_square == ' ':
        return stop_packet
    else:
        packet.add_letter(next_square)
        return move_north


def move_west(grid, packet, pos):
    pos.x -= 1
    next_square = grid[pos.y][pos.x]
    if next_square == '|' or next_square == '-':
        # Continue west
        return move_west
    elif next_square == '+':
        # Change direction
        if grid[pos.y - 1][pos.x] == ' ':
            # North is blank, move South
            return move_south
        else:
            return move_north
    elif next_square == ' ':
        return stop_packet
    else:
        packet.add_letter(next_square)
        return move_west


def move_east(grid, packet, pos):
    pos.x += 1
    next_square = grid[pos.y][pos.x]
    if next_square == '|' or next_square == '-':
        # Continue east
        return move_east
    elif next_square == '+':
        # Change direction
        if grid[pos.y - 1][pos.x] == ' ':
            # North is blank, move South
            return move_south
        else:
            return move_north
    elif next_square == ' ':
        return stop_packet
    else:
        packet.add_letter(next_square)
        return move_east


def move_south(grid, packet, pos):
    pos.y += 1
    next_square = grid[pos.y][pos.x]
    if next_square == '|' or next_square == '-':
        # Continue south
        return move_south
    elif next_square == '+':
        # Change direction
        if grid[pos.y][pos.x - 1] == ' ':
            # West is blank, move East
            return move_east
        else:
            return move_west
    elif next_square == ' ':
        return stop_packet
    else:
        packet.add_letter(next_square)
        return move_south


def main(argv):
    diagram = load_input(argv[1])
    # for line in diagram:
    #     print(line)
    pos = find_start_pos(diagram)
    print('Starting at %r' % (pos))
    # Packet is a list of letters encountered
    packet = Packet()
    mover = move_south
    while True:
        mover = mover(diagram, packet, pos)


if __name__ == '__main__':
    main(sys.argv)
