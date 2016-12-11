#!/usr/bin/env python

import sys

def is_abba(input):
    return (input[0] == input[3] and
            input[1] == input[2] and
            input[0] != input[1])

def has_abba_old(input):
    in_hypernet = False
    has_abba = False
    has_hypernet_abba = False
    for x in range(len(input) - 4):
        if input[x] == '[':
            in_hypernet = True
            continue
        if input[x] == ']':
            in_hypernet = False
            continue
        if is_abba(input[x:]):
            if in_hypernet:
                has_hypernet_abba = True
            else:
                has_abba = True
    return has_abba and not has_hypernet_abba

def has_abba2(input):
    print 'has_abba2', input
    x = input
    while len(x) >= 4:
        if is_abba(x):
            return True
        x = x[1:]
    return False

def get_delimiter(x):
    if x:
        return ']'
    else:
        return '['

def has_abba(input):
    in_hypernet = False
    has_abba = False
    has_hypernet_abba = False
    x = input
    while x:
        delim = get_delimiter(in_hypernet)
        if delim in x:
            pos = x.index(delim)
        else:
            pos = len(x)
        abba = has_abba2(x[0:pos])
        print 'abba for', x[0:pos], '=', abba
        if abba:
            if in_hypernet:
                has_hypernet_abba = True
            else:
                has_abba = True
        x = x[pos+1:]
        in_hypernet = not in_hypernet
    return has_abba and not has_hypernet_abba

def parse_data(datafile):
    tls_count = 0
    with open(datafile, 'rb') as f:
        for line in f:
            line = line.strip()
            tls = has_abba(line)
            # print line, tls
            if tls:
                tls_count += 1
    print tls_count

def main(argv):
    datafile = argv[1]
    parse_data(datafile)

# The answer is NOT 114
# 109 is too low
# 115 is correct

if __name__ == '__main__':
    main(sys.argv)
