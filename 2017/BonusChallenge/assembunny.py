#!/usr/bin/env python3

import sys


def load_program(filename):
    with open(filename, 'rb') as f:
        return [l.strip().decode('utf-8').split() for l in f.readlines()]


def get_value(item, registers):
    if item in registers:
        return registers[item]
    else:
        return int(item)


def toggle(prog, pc, registers):
    # print 'toggle:', prog[pc]
    target_idx = pc + get_value(prog[pc][1], registers)
    # If an attempt is made to toggle an instruction outside the program,
    # nothing happens
    if target_idx < 0 or target_idx >= len(prog):
        return
    target = prog[target_idx]
    if len(target) == 2:
        if target[0] == 'inc':
            target[0] = 'dec'
        else:
            target[0] = 'inc'
    elif len(target) == 3:
        if target[0] == 'jnz':
            target[0] = 'cpy'
        else:
            target[0] = 'jnz'


def execute(prog, pc, registers):
    cmd = prog[pc]
    # print('Executing', pc, ':', cmd, registers)
    inst = cmd[0]
    if inst == 'cpy':
        x = cmd[1]
        if x in registers:
            registers[cmd[2]] = registers[x]
        else:
            registers[cmd[2]] = int(x)
    elif inst == 'inc':
        registers[cmd[1]] = registers[cmd[1]] + 1
    elif inst == 'dec':
        registers[cmd[1]] = registers[cmd[1]] - 1
    elif inst == 'jnz':
        x = get_value(cmd[1], registers)
        y = get_value(cmd[2], registers)
        if x:
            return pc + y
    elif inst == 'tgl':
        toggle(prog, pc, registers)
    elif inst == 'out':
        x = cmd[1]
        if x in registers:
            outval = registers[x]
        else:
            outval = int(x)
        # print("Out: %r (%r)" % (outval, str(chr(outval))))
        sys.stdout.write(str(chr(outval)))
    return pc + 1


def main(argv=None):
    if not argv:
        argv = sys.argv
    prog = load_program(argv[1])
    # print(prog)
    registers = {'a': 12, 'b': 0, 'c': 0, 'd': 0}
    pc = 0
    while pc < len(prog):
        pc = execute(prog, pc, registers)
    # print(registers)


if __name__ == '__main__':
    main()
