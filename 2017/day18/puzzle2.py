#!/usr/bin/env python3

# http://adventofcode.com/2017/day/18

import collections
import sys

TRACE = True
PC = 'pc'
RECEIVE = 'rcv'
SEND = 'snd'
TERMINATED = 'trm'
BLOCKED = 'blk'
SENT = 'snt'


# Data is one command per line
def load_input(datafile):
    with open(datafile, 'rb') as f:
        return [line.rstrip().decode('utf-8') for line in f]


def duet_snd(pc, regs, reg):
    if TRACE:
        print('Send %d' % (regs[reg]))
    regs[SEND].insert(0, regs[reg])
    regs[SENT] += 1
    return pc + 1


def duet_compile_snd(command, reg):
    return lambda pc, regs: duet_snd(pc, regs, reg)


def duet_set_int(pc, regs, reg, val):
    if TRACE:
        print('Set %s to %d' % (reg, val))
    regs[reg] = val
    return pc + 1


def duet_set(pc, regs, reg, var):
    if TRACE:
        print('Set %s to %s (%d)' % (reg, var, regs[var]))
    return duet_set_int(pc, regs, reg, regs[var])


def duet_compile_set(command, reg, val):
    try:
        val = int(val)
        return lambda pc, regs: duet_set_int(pc, regs, reg, val)
    except ValueError:
        return lambda pc, regs: duet_set(pc, regs, reg, val)


def duet_add_int(pc, regs, reg, val):
    if TRACE:
        print('Add %s to %d' % (reg, val))
    regs[reg] += val
    return pc + 1


def duet_add(pc, regs, reg, var):
    if TRACE:
        print('Add %s to %s (%d)' % (reg, var, regs[var]))
    return duet_add_int(pc, regs, reg, regs[var])


def duet_compile_add(command, reg, val):
    try:
        val = int(val)
        return lambda pc, regs: duet_add_int(pc, regs, reg, val)
    except ValueError:
        return lambda pc, regs: duet_add(pc, regs, reg, val)


def duet_mul_int(pc, regs, reg, val):
    if TRACE:
        print('mul %s by %d' % (reg, val))
    regs[reg] *= val
    return pc + 1


def duet_mul(pc, regs, reg, var):
    if TRACE:
        print('mul %s by %s (%d)' % (reg, var, regs[var]))
    return duet_mul_int(pc, regs, reg, regs[var])


def duet_compile_mul(command, reg, val):
    try:
        val = int(val)
        return lambda pc, regs: duet_mul_int(pc, regs, reg, val)
    except ValueError:
        return lambda pc, regs: duet_mul(pc, regs, reg, val)


def duet_mod_int(pc, regs, reg, val):
    if TRACE:
        print('mod %s by %d' % (reg, val))
    regs[reg] %= val
    return pc + 1


def duet_mod(pc, regs, reg, var):
    if TRACE:
        print('mod %s by %s (%d)' % (reg, var, regs[var]))
    return duet_mod_int(pc, regs, reg, regs[var])


def duet_compile_mod(command, reg, val):
    try:
        val = int(val)
        return lambda pc, regs: duet_mod_int(pc, regs, reg, val)
    except ValueError:
        return lambda pc, regs: duet_mod(pc, regs, reg, val)


def duet_rcv(pc, regs, reg):
    if TRACE:
        print('rcv %s (%d)' % (reg, regs[reg]))
    rcvq = regs[RECEIVE]
    if rcvq:
        regs[reg] = rcvq.pop()
        regs[BLOCKED] = 0
        return pc + 1
    else:
        regs[BLOCKED] += 1
        return pc


def duet_compile_rcv(command, reg):
    return lambda pc, regs: duet_rcv(pc, regs, reg)


def duet_jgz(pc, regs, val, jump):
    if val > 0:
        return pc + jump
    else:
        return pc + 1


def duet_jgz_v_c(pc, regs, var, jump):
    return duet_jgz(pc, regs, regs[var], jump)


def duet_jgz_c_v(pc, regs, val, jump_var):
    return duet_jgz(pc, regs, val, regs[jump_var])


def duet_jgz_v_v(pc, regs, var, jump_var):
    return duet_jgz(pc, regs, regs[var], regs[jump_var])


def duet_compile_jgz_c(command, val, jump_reg):
    try:
        jump_reg = int(jump_reg)
        return lambda pc, regs: duet_jgz(pc, regs, val, jump_reg)
    except ValueError:
        return lambda pc, regs: duet_jgz_c_v(pc, regs, val, jump_reg)


def duet_compile_jgz_v(command, val, jump_reg):
    try:
        jump_reg = int(jump_reg)
        return lambda pc, regs: duet_jgz_v_c(pc, regs, val, jump_reg)
    except ValueError:
        return lambda pc, regs: duet_jgz_v_v(pc, regs, val, jump_reg)


def duet_compile_jgz(command, reg, jump_reg):
    try:
        reg = int(reg)
        return duet_compile_jgz_c(command, reg, jump_reg)
    except ValueError:
        return duet_compile_jgz_v(command, reg, jump_reg)


def duet_compile(command):
    cmd = command[0:3]
    print(cmd)
    if cmd == 'snd':
        return duet_compile_snd(*command.split())
    elif cmd == 'set':
        return duet_compile_set(*command.split())
    elif cmd == 'add':
        return duet_compile_add(*command.split())
    elif cmd == 'mul':
        return duet_compile_mul(*command.split())
    elif cmd == 'mod':
        return duet_compile_mod(*command.split())
    elif cmd == 'rcv':
        return duet_compile_rcv(*command.split())
    elif cmd == 'jgz':
        return duet_compile_jgz(*command.split())
    return None


def duet_run(commands, regs):
    pc = regs[PC]
    pc = commands[pc](pc, regs)
    if pc < 0 or pc >= len(commands):
        regs[TERMINATED] = True
    regs[PC] = pc


def main(argv):
    commands = load_input(argv[1])
    commands = [duet_compile(cmd) for cmd in commands]
    # Program 0
    regs0 = collections.defaultdict(int)
    regs0['p'] = 0
    regs0[SEND] = []
    regs0[RECEIVE] = []
    regs0[PC] = 0
    regs0[TERMINATED] = False
    # Program 1
    regs1 = collections.defaultdict(int)
    regs1['p'] = 1
    regs1[SEND] = regs0[RECEIVE]
    regs1[RECEIVE] = regs0[SEND]
    regs1[PC] = 0
    regs1[TERMINATED] = False
    while not regs0[TERMINATED] and not regs1[TERMINATED]:
        duet_run(commands, regs0)
        duet_run(commands, regs1)
        if regs0[BLOCKED] > 10 and regs1[BLOCKED] > 10:
            print('Deadlock')
            break
    print('program 1 sent %d values.' % (regs1[SENT]))


if __name__ == '__main__':
    main(sys.argv)
