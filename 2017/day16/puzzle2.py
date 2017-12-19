#!/usr/bin/env python3

# http://adventofcode.com/2017/day/16

# Wrong answer:
#
# nechdblkjmgpfaoi
# pabheomkcjfndlig
# iadfhebgjmloncpk
#

import collections
import sys

A_BILLION = 1000000000


# Data is all on one line
def load_input(datafile):
    with open(datafile, 'rb') as f:
        return f.read().decode('utf-8').rstrip().split(',')


def swap(progs, a, b):
    # print('swap(%r, %r)' % (a, b))
    progs[a], progs[b] = progs[b], progs[a]


def partner(progs, char_a, char_b):
    # print('partner(%r, %r)' % (char_a, char_b))
    swap(progs, progs.index(char_a), progs.index(char_b))


def compile_move(move):
    if move[0] == 's':
        arg = int(move[1:])
        return lambda p: p.rotate(arg)
    elif move[0] == 'x':
        tmp = move[1:].split('/')
        arg0 = int(tmp[0])
        arg1 = int(tmp[1])
        return lambda p: swap(p, arg0, arg1)
    elif move[0] == 'p':
        tmp = move[1:].split('/')
        arg0 = tmp[0]
        arg1 = tmp[1]
        return lambda p: partner(p, arg0, arg1)


def find_cycle(progs, moves):
    all_progs = {''.join(progs): 0}
    for i in range(A_BILLION):
        for move in moves:
            move(progs)
        str_progs = ''.join(progs)
        print('After move %d: %r' % (i + 1, str_progs))
        if str_progs in all_progs:
            a = all_progs[str_progs]
            print('Cycle detected at %r and %r' % (a, i))
            print('Progs = %r' % (progs))
            return(progs, a, i)
        else:
            all_progs[str_progs] = i


def main(argv):
    # progs = 'abcde'
    progs = 'abcdefghijklmnop'
    progs = collections.deque(progs)

    datafile = argv[1]
    moves = load_input(datafile)
    moves = [compile_move(m) for m in moves]

    (cycle_progs, cycle_a, cycle_b) = find_cycle(progs, moves)
    remaining_cycles = A_BILLION - cycle_a
    cycles_to_go = remaining_cycles % (cycle_b - cycle_a + 1)
    print('Starting final pass with %r' % (''.join(cycle_progs)))
    print('Running %d more cycles' % (cycles_to_go))
    for i in range(cycles_to_go):
        for move in moves:
            move(cycle_progs)
    print(''.join(cycle_progs))


if __name__ == '__main__':
    main(sys.argv)
