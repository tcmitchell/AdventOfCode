#!/usr/bin/env python

import md5
import sys

def main(argv=None):
    if not argv:
        argv = sys.argv
    seed = argv[1]
    i = 1
    while True:
        x = md5.md5(seed + str(i)).hexdigest()
        if x.startswith('00000'):
            print 'Found 5 zeroes at', i
            break
        i += 1

if __name__ == '__main__':
    main()
