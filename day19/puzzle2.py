#!/usr/bin/env python

import sys

class Elf(object):

    def __init__(self, id, next, prev):
        self.id = id
        self.presents = 1
        self.next = next
        self.prev = prev

    def __repr__(self):
        return 'Elf(%d, %d, %d)' % (self.id, self.next, self.prev)

    def __str__(self):
        return 'Elf #%d' % (self.id)

def make_elves(count):
    elves = {}
    for i in range(count):
        id = i + 1
        elves[id] = Elf(id, id+1, id-1)
    # Now fix up first and last
    # print elves
    elves[1].prev = count
    elves[count].next = 1
    return elves

def main(argv=None):
    if not argv:
        argv = sys.argv
    count = int(argv[1])
    elves = make_elves(count)
    elf = 1
    del_ptr = count / 2 + elf
    while count > 1:
        # Maintain a delete pointer, otherwise the time
        # required is astronimical
        grabber = elves[elf]
        grabbee = elves[del_ptr]
        print 'Elf %d grabs from elf %d' % (grabber.id, grabbee.id)
        grabber.presents += grabbee.presents
        # Unlink the empty elf
        elves[grabbee.prev].next = grabbee.next
        elves[grabbee.next].prev = grabbee.prev
        del elves[grabbee.id]
        # Adjust the pointers
        count -= 1
        elf = grabber.next
        del_ptr = grabbee.next
        # If there are an even number of elves now, advance the delete
        # pointer one more
        if count % 2 == 0:
            del_ptr = elves[del_ptr].next
    print '%d has %d presents' % (elf, elves[elf].presents)

if __name__ == '__main__':
    main()
