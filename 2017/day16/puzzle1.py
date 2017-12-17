#!/usr/bin/env python3

# http://adventofcode.com/2017/day/16

import sys


# Data is all on one line
def load_input(datafile):
    with open(datafile, 'rb') as f:
        return f.read().decode('utf-8').rstrip().split(',')


def spin(progs, count):
    print('spin(%r, %r)' % (progs, count))
    return progs[-count:] + progs[0:-count]


def swap(progs, pos_a, pos_b):
    print('swap(%r, %r)' % (pos_a, pos_b))
    prog_list = list(progs)
    print('swap list = %r' % (prog_list))
    tmp = prog_list[pos_a]
    prog_list[pos_a] = prog_list[pos_b]
    prog_list[pos_b] = tmp
    return ''.join(prog_list)


def partner(progs, char_a, char_b):
    print('partner(%r, %r)' % (char_a, char_b))
    return swap(progs, progs.find(char_a), progs.find(char_b))


def perform_move(progs, move):
    print('Performing move %r' % (move))
    if move[0] == 's':
        progs = spin(progs, int(move[1:]))
    elif move[0] == 'x':
        tmp = move[1:].split('/')
        progs = swap(progs, int(tmp[0]), int(tmp[1]))
    elif move[0] == 'p':
        tmp = move[1:].split('/')
        progs = partner(progs, tmp[0], tmp[1])
    print('Move result: %r' % (progs))
    return progs


def main(argv):
    progs = 'abcde'
    progs = 'abcdefghijklmnop'
    datafile = argv[1]
    moves = load_input(datafile)
    print(moves)
    for move in moves:
        progs = perform_move(progs, move)
    print(progs)


if __name__ == '__main__':
    main(sys.argv)
