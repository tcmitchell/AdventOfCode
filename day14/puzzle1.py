#!/usr/bin/env python

import re
import sys
import md5


def main(argv=None):
    if not argv:
        argv = sys.argv
    salt = argv[1]
    triple_prog = re.compile(r'(.)\1\1')
    i = 0
    keys = []
    while len(keys) < 10:
        data = md5.md5(salt + str(i)).hexdigest()
        m = triple_prog.search(data)
        if m:
            keys.append((data, m.group(1), i+1000))
        i += 1
    print keys


if __name__ == '__main__':
    main()
