#!/usr/bin/env python3

# http://adventofcode.com/2017/day/20

# Wrong answer:
#
#  413

import re
import sys


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Point(%r, %r, %r)' % (self.x, self.y, self.z)


class Particle:
    input_re = re.compile('^p=<(.*)>, v=<(.*)>, a=<(.*)>$')

    @classmethod
    def from_input(cls, pnum, line):
        match = Particle.input_re.match(line)
        if match:
            args = [pnum]
            for g in match.groups():
                args.append(Point(*[int(d) for d in g.split(',')]))
            return Particle(*args)
            print(args)
        else:
            print('No match')

    def __init__(self, pnum, pos, vel, acc):
        self.pnum = pnum
        self.pos = pos
        self.vel = vel
        self.acc = acc
        # Distance Score
        self.dscore = 0

    def __repr__(self):
        return 'Particle(%r, %r, %r, %r)' % (self.pnum, self.pos, self.vel,
                                             self.acc)

    def tick(self):
        self.vel.x += self.acc.x
        self.vel.y += self.acc.y
        self.vel.z += self.acc.z
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z

    def distance(self):
        # Return the sum of the absolute values of the position
        return sum(map(abs, [self.pos.x, self.pos.y, self.pos.z]))

    def add_score(self, score):
        self.dscore += score


def load_input(datafile):
    with open(datafile, 'rb') as f:
        return [line.decode('utf-8').rstrip() for line in f]


def tick_and_score(particles):
    for p in particles:
        p.tick()
        # print(p)
    scores = sorted(particles, key=Particle.distance)
    for ind, p in enumerate(scores):
        p.add_score(ind)


def main(argv):
    datafile = argv[1]
    raw_data = load_input(datafile)
    particles = [Particle.from_input(ind, line)
                 for ind, line in enumerate(raw_data)]
    print(particles)
    for tick in range(10000):
        tick_and_score(particles)
        # print()
    results = sorted(particles, key=lambda p: p.dscore)
    print('Closest = %r' % (results[0]))
    print('Currently closest = %r' %
          (sorted(particles, key=Particle.distance)[0]))


if __name__ == '__main__':
    main(sys.argv)
