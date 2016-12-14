#!/usr/bin/env python

import re
import sys
import md5
import pprint

def make_quint_prog(char):
    return re.compile(r'(%c)\1\1\1\1' % (char))

def main(argv=None):
    if not argv:
        argv = sys.argv
    salt = argv[1]
    triple_prog = re.compile(r'(.)\1\1')
    i = 0
    candidates = []
    keys = []
    while len(keys) < 64:
        # Remove expired candidates
        candidates = [c for c in candidates if i <= c[2]]
        # Remove candidates that are already keys
        candidates = [c for c in candidates if c[0] not in [k[0] for k in keys]]
        # Look at next candidate
        data = md5.md5(salt + str(i)).hexdigest()
        # Check for key in previous candidates
        for cand in candidates:
            (key, prog, expires) = cand
            m = prog.search(data)
            if m:
                keys.append((key, expires-1000, i))
        # Check for new candidate
        m = triple_prog.search(data)
        if m:
            prog = make_quint_prog(m.group(1))
            expires = i + 1000
            candidates.append((data, prog, expires))
        i += 1
    # pprint.pprint(keys)
    print 'The 64th key was at index', keys[63][1]

# 24438 is too high

if __name__ == '__main__':
    main()
