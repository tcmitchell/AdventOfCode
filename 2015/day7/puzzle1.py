#!/usr/bin/env python3

import pprint
import re
import sys
import time

assign_int_prog = re.compile(r'(\d+)')
assign_var_prog = re.compile(r'(.+)')
not_prog = re.compile(r'NOT (.+)')
and_prog = re.compile(r'(.+) AND (.+)')
or_prog = re.compile(r'(.+) OR (.+)')
lshift_prog = re.compile(r'(.+) LSHIFT (.+)')
rshift_prog = re.compile(r'(.+) RSHIFT (.+)')


def parse_input(filename):
    prog = re.compile(r'(.*) -> (.*)')
    conns = []
    with open(filename, 'rb') as f:
        for line in f:
            m = prog.match(line.decode('utf-8').strip('\n'))
            if m:
                conns.append(m.groups())
    return conns


def int_or_var(wires, thing):
    try:
        return int(thing)
    except ValueError:
        if thing in wires:
            return wires[thing]
        else:
            return None


def handle_assign_int(wires, rhs, val):
    wires[rhs] = int(val)
    return True


def handle_assign_var(wires, rhs, var):
    print('assign_var(%r, %r)' % (rhs, var))
    if var in wires:
        wires[rhs] = wires[var]
        return True
    else:
        return False


def handle_not(wires, rhs, var):
    if var in wires:
        wires[rhs] = ~wires[var]
        if wires[rhs] < 0:
            wires[rhs] += 65536
        return True
    else:
        return False


def handle_and(wires, rhs, l, r):
    x = int_or_var(wires, l)
    y = int_or_var(wires, r)
    if x and y:
        wires[rhs] = x & y
        return True
    else:
        return False


def handle_or(wires, rhs, l, r):
    if l in wires and r in wires:
        wires[rhs] = wires[l] | wires[r]
        return True
    else:
        return False


def handle_lshift(wires, rhs, var, x):
    if var in wires:
        wires[rhs] = wires[var] << int(x)
        return True
    else:
        return False


def handle_rshift(wires, rhs, var, x):
    if var in wires:
        wires[rhs] = wires[var] >> int(x)
        return True
    else:
        return False


handlers = [
    (not_prog, handle_not),
    (and_prog, handle_and),
    (or_prog, handle_or),
    (lshift_prog, handle_lshift),
    (rshift_prog, handle_rshift),
    (assign_int_prog, handle_assign_int),
    (assign_var_prog, handle_assign_var)
]


def process_conn(wires, c):
    (l, r) = c
    for (rx, func) in handlers:
        m = rx.match(l)
        if m:
            print('%r(%r, %r)' % (func, r, m.groups()))
            return func(wires, r, *m.groups())
    raise Exception('No match for %r' % (l))
    return False


def main(argv=None):
    if not argv:
        argv = sys.argv
    infile = argv[1]
    conns = parse_input(infile)
    pprint.pprint(conns)
    wires = {}
    done = []
    while conns:
        for c in conns:
            if process_conn(wires, c):
                done.append(c)
        for c in done:
            conns.remove(c)
        done = []
        pprint.pprint(wires)
        print('=====')
        pprint.pprint(conns)
        print('%d connections remain' % (len(conns)))
        time.sleep(1)


if __name__ == '__main__':
    main()
