#!/usr/bin/env python

import sys

class Elf(object):

    def __init__(self, id, next=None):
        self.id = id
        self.presents = 1
        self.next = next

    def __repr__(self):
        return 'Elf(%r)' % (self.id)

    def __str__(self):
        return 'Elf #%d' % (self.id)

    def grab(self):
        self.presents += self.next.presents
        self.next = self.next.next

def make_elves(count):
    last = Elf(count)
    next = last
    while count > 1:
        count -= 1
        elf = Elf(count, next)
        next = elf
    last.next = elf
    return elf

def main(argv=None):
    if not argv:
        argv = sys.argv
    count = int(argv[1])
    elves = make_elves(count)
    # elf = elves
    # print elf
    # while elf.next != elves:
    #     print elf.next
    #     elf = elf.next
    elf = elves
    while elf.next != elf:
        elf.grab()
        elf = elf.next
    print 'Elf %r has %d presents' % (elf, elf.presents)


if __name__ == '__main__':
    main()
