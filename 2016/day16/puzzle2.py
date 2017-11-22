#!/usr/bin/env python

import sys

def dragon(b):
    # reverse the string
    b = b[::-1]
    # change 1 to 0 and vice versa
    # print 'before', b
    b = b.replace('1', '2')
    # print '1->2', b
    b = b.replace('0', '1')
    # print '0->1', b
    b = b.replace('2', '0')
    # print '2->0', b
    return b

def checksum_pair(p):
    if p[0] == p[1]:
        return '1'
    else:
        return '0'

def checksum(a):
    n = 2
    x = [a[i:i+n] for i in range(0, len(a), n)]
    return ''.join([checksum_pair(z) for z in x])

def test_dragon(input, output):
    a = input + '0' + dragon(input)
    if a == output:
        print 'PASS'
    else:
        print 'FAIL: input =', input, '; output =', output, '; a =', a

def test():
    test_dragon('1', '100')
    test_dragon('0', '001')
    test_dragon('11111', '11111000000')
    test_dragon('111100001010', '1111000010100101011110000')

# 01110011101111011 is too low - had 272 hardcoded

def main(argv=None):
    if not argv:
        argv = sys.argv
    test()
    a = argv[1]
    disk_length = 35651584
    while len(a) < disk_length:
        a = a + '0' + dragon(a)
    a = a[0:disk_length]
    c = a
    while len(c) % 2 == 0:
        c = checksum(c)
    print c

if __name__ == '__main__':
    main()
