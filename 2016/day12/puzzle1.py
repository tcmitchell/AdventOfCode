#!/usr/bin/env python

import sys

def load_program(filename):
    with open(filename, 'rb') as f:
        return [l.strip().split() for l in f.readlines()]

def execute(prog, pc, registers):
    cmd = prog[pc]
    print 'Executing', cmd
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
        x = cmd[1]
        if x in registers:
            if registers[x]:
                return pc + int(cmd[2])
        elif int(x):
            return pc + int(cmd[2])
    return pc + 1

def main(argv=None):
    if not argv:
        argv = sys.argv
    prog = load_program(argv[1])
    print prog
    registers = {'a':0, 'b':0, 'c':0, 'd':0}
    pc = 0
    while pc < len(prog):
        pc = execute(prog, pc, registers)
    print registers

if __name__ == '__main__':
    main()
