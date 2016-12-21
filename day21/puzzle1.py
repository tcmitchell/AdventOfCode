#!/usr/bin/env python

import pprint
import re
import sys

swap_pos_prog = re.compile(r'swap position (\d+) with position (\d+)')
swap_ltr_prog = re.compile(r'swap letter (.) with letter (.)')
reverse_prog = re.compile(r'reverse positions (\d+) through (\d+)')
rotatel_prog = re.compile(r'rotate left (\d+) step')
rotater_prog = re.compile(r'rotate right (\d+) step')
move_prog = re.compile(r'move position (\d+) to position (\d+)')
rotatep_prog = re.compile(r'rotate based on position of letter (.)')

def load_instructions(infile):
    with open(infile, 'rb') as f:
        return [l.strip() for l in f]

def handle_swap_pos(password, match):
    (pos1, pos2) = (int(x) for x in match.groups())
    # print (pos1, pos2)
    password[pos1], password[pos2] = password[pos2], password[pos1]
    return password

def handle_swap_ltr(password, match):
    (ltr1, ltr2) = match.groups()
    pos1, pos2 = password.index(ltr1), password.index(ltr2)
    password[pos1], password[pos2] = password[pos2], password[pos1]
    return password

def handle_reverse(password, match):
    (pos1, pos2) = (int(x) for x in match.groups())
    result = password[0:pos1]
    result.extend(reversed(password[pos1:pos2+1]))
    result.extend(password[pos2+1:])
    return result

def handle_dummy(password, match):
    pass

def rotate(password, n):
    passlen = len(password)
    if abs(n) > passlen:
        n = n % passlen
    return password[n:] + password[:n]

def handle_rotate_left(password, match):
    n = int(match.group(1))
    return rotate(password, n)

def handle_rotate_right(password, match):
    n = int(match.group(1))
    return rotate(password, -n)

def handle_move(password, match):
    (pos1, pos2) = (int(x) for x in match.groups())
    password.insert(pos2, password.pop(pos1))
    return password

def handle_rotate_pos(password, match):
    ltr = match.group(1)
    idx = password.index(ltr)
    rots = 1 + idx
    if idx >= 4:
        rots += 1
    print 'rotations', -rots
    return rotate(password, -rots)

handlers = [
    (swap_pos_prog, handle_swap_pos),
    (swap_ltr_prog, handle_swap_ltr),
    (reverse_prog, handle_reverse),
    (rotatel_prog, handle_rotate_left),
    (rotater_prog, handle_rotate_right),
    (move_prog, handle_move),
    (rotatep_prog, handle_rotate_pos)
]

def main(argv=None):
    if not argv:
        argv = sys.argv
    infile = argv[1]
    password = [l for l in argv[2]]
    instrs = load_instructions(infile)
    for instr in instrs:
        handled = False
        for (prog, func) in handlers:
            match = prog.match(instr)
            if match:
                password = func(password, match)
                handled = True
                break
        if not handled:
            raise Exception('Unhandled instruction: %r' % (instr))
    print password
    print ''.join(password)


if __name__ == '__main__':
    main()
