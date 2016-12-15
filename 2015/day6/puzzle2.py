#!/usr/bin/env python

import re
import sys

prog = re.compile(r'(.*) (\d+),(\d+) through (\d+),(\d+)')

OFF = 0

def turn_on(lights, cmd, x1, y1, x2, y2):
    (x1, y1, x2, y2) = (int(z) for z in (x1, y1, x2, y2))
    print 'turn_on(%r, %r, %r, %r)' % (x1, y1, x2, y2)
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            lights[x][y] += 1

def turn_off(lights, cmd, x1, y1, x2, y2):
    (x1, y1, x2, y2) = (int(z) for z in (x1, y1, x2, y2))
    print 'turn_off(%r, %r, %r, %r)' % (x1, y1, x2, y2)
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            if lights[x][y] == 0:
                continue
            lights[x][y] -= 1

def toggle(lights, cmd, x1, y1, x2, y2):
    (x1, y1, x2, y2) = (int(z) for z in (x1, y1, x2, y2))
    print 'toggle(%r, %r, %r, %r)' % (x1, y1, x2, y2)
    for x in range(x1, x2+1):
        for y in range(y1, y2+1):
            lights[x][y] += 2

commands = {
    'turn on': turn_on,
    'turn off': turn_off,
    'toggle': toggle
}

def process_command(lights, line):
    # print line
    m = prog.match(line)
    if m:
        func = commands[m.group(1)]
        func(lights, *m.groups())
    else:
        print 'no match'

def process_commands(lights, filename):
    with open(filename, 'rb') as f:
        for line in f:
            process_command(lights, line)

def main(argv=None):
    if not argv:
        argv = sys.argv
    lights = []
    for x in range(1000):
        lights.append([0]*1000)
    process_commands(lights, argv[1])
    lights_on = 0
    for x in range(1000):
        lights_on += sum(lights[x])
    print 'total brightness is', lights_on

# 14747699 is too low
# 15343601 is correct -- there's a minimum brightness of zero

if __name__ == '__main__':
    main()
