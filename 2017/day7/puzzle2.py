#!/usr/bin/env python3

# http://adventofcode.com/2017/day/7

# Answer 913 is too high


import re
import sys


class Program():

    # name_weight_re = re.compile('^(\w+) \((\d)\)')
    name_weight_re = re.compile('^(\w+) \((\d+)\)')

    def __init__(self, name, weight, supports=[]):
        self.name = name
        self.weight = weight
        self.supports = supports
        self.depth = None
        self.computed_weight = 0

    def compute_weight_and_depth(self, all_programs):
        if self.depth is not None:
            print('%s is already computed' % (self.name))
            return
        if not self.supports:
            print('%s is a leaf' % (self.name))
            self.depth = 0
            self.computed_weight = self.weight
            return
        progs = [all_programs[s] for s in self.supports]
        for p in progs:
            p.compute_weight_and_depth(all_programs)
        weights = [p.computed_weight for p in progs]
        # children = [(p.depth, p.computed_weight) for p in progs]
        test = set(weights)
        if len(test) != 1:
            print('Program %r is unbalanced: %r' % (self.name, weights))
            for p in progs:
                print('Child %s: %d' % (p.name, p.computed_weight))
        self.depth = progs[0].depth + 1
        self.computed_weight = sum(weights) + self.weight
        print('%s has depth %d, computed weight %d' %
              (self.name, self.depth, self.computed_weight))

    @classmethod
    def from_input(cls, line):
        """The lines take two forms:

        1. name (###)
        2. name (###) -> name, name, name
        """
        x = line.split('->')
        match = Program.name_weight_re.match(x[0])
        if not match:
            raise Exception('No match on %r' % (line))
        else:
            name = match.group(1)
            weight = int(match.group(2))
        if len(x) > 1:
            supports = [n.strip() for n in x[1].split(',')]
            return Program(name, weight, supports)
        else:
            return Program(name, weight)


def load_input(datafile):
    with open(datafile, 'rb') as f:
        return [line.decode('utf-8').rstrip() for line in f]


def parse_input(raw_data, programs, supported):
    """The lines take two forms:

    1. name (###)
    2. name (###) -> name, name, name
    """
    for line in raw_data:
        x = line.split('->')
        prog = x[0].split()[0]
        programs.append(prog)
        # print(prog)
        if len(x) > 1:
            sup = [n.strip() for n in x[1].split(',')]
            supported.extend(sup)


def main(argv):
    datafile = argv[1]
    raw_data = load_input(datafile)
    programs = [Program.from_input(x) for x in raw_data]
    print('Found %d programs' % (len(programs)))
    # for p in programs:
    #     print('%s (%d) -> %r' % (p.name, p.weight, p.supports))
    all_programs = {p.name: p for p in programs}
    # print('%s: %r' % ('fwft', all_programs['fwft']))
    for p in all_programs.values():
        p.compute_weight_and_depth(all_programs)


if __name__ == '__main__':
    main(sys.argv)
