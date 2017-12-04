#!/usr/bin/env python3

# http://adventofcode.com/2017/day/4

import sys


def load_passphrases(datafile):
    with open(datafile, 'rb') as f:
        return [line.decode('utf-8').strip('\n') for line in f]


def main(argv):
    datafile = argv[1]
    passphrases = load_passphrases(datafile)
    valid = 0
    invalid = 0
    for phrase in passphrases:
        words = phrase.split(' ')
        exploded = [''.join(sorted(list(word))) for word in words]
        word_set = set(exploded)
        if len(words) == len(word_set):
            valid += 1
        else:
            invalid += 1
    print('Loaded %d passphrases' % (len(passphrases)))
    print('Found %d valid' % (valid))
    print('Found %d invalid' % (invalid))


if __name__ == '__main__':
    main(sys.argv)
