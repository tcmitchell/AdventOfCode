#!/usr/bin/env python

import re
import sys

vowel_prog = re.compile(r'[aeiou]')

# two letters in a row
# letters are not non-alphanumeric, not digit, and not underscore
double_letter_prog = re.compile(r'([^\W\d_])\1')

prog3 = re.compile(r'ab|cd|pq|xy')


def has3vowels(string):
    return len(vowel_prog.findall(string)) > 2

def has_double_letter(string):
    return double_letter_prog.search(string)

def has_bad_sequence(string):
    return prog3.search(string)

def is_nice(string):
    return (has3vowels(string) and
            has_double_letter(string) and
            not has_bad_sequence(string))

def nice_strings(filename):
    with open(filename, 'rb') as f:
        return [x for x in f if is_nice(x)]

def main(argv=None):
    if not argv:
        argv = sys.argv
    ns = nice_strings(argv[1])
    print 'Found %d nice strings' % (len(ns))

if __name__ == '__main__':
    main()
