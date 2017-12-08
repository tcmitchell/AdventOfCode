#!/usr/bin/env python3

# http://adventofcode.com/2017/day/8

import collections
import sys


# See https://stackoverflow.com/questions/26987418/programmatically-create-function-specification
def make_orig_fun(parameters):
    exec("def f_make_fun(r):\n    if r['a'] > 1:\n        r['b'] += 5".format(', '.join(parameters)))
    return locals()['f_make_fun']


def make_instr(t_var, t_op, t_val, d_var, d_op, d_val):
    """Makes an instruction function using test (t_) and
    destination(d_) information.
    t_var = test var; t_op = test operator; t_val = test_value
    d_var = dest var; d_op = dest operator; d_val = dest_value
    """
    f_tmpl = """def _aoc_func(r):
        if r['%s'] %s %s:
            r['%s'] %s %s
    """
    exec(f_tmpl % (t_var, t_op, t_val, d_var, d_op, d_val))
    return locals()['_aoc_func']


def load_input(datafile):
    with open(datafile, 'rb') as f:
        return [line.decode('utf-8').rstrip() for line in f]


def parse_d_op(raw_op):
    if raw_op == 'inc':
        return '+='
    elif raw_op == 'dec':
        return '-='
    else:
        raise Exception('Unknown d_op %s' % (raw_op))


def parse_instruction(raw):
    """Returns a python function corresponding to the input
    string. Inputs take the form:

       b inc 5 if a > 1
       a inc 1 if b < 5
       c dec -10 if a >= 1
       c inc -20 if c == 10
    """
    parts = raw.split()
    d_var = parts[0]
    d_op = parse_d_op(parts[1])
    d_val = parts[2]
    t_var = parts[4]
    t_op = parts[5]
    t_val = parts[6]
    return make_instr(t_var, t_op, t_val, d_var, d_op, d_val)


def main(argv):
    datafile = argv[1]
    raw_data = load_input(datafile)
    instrs = [parse_instruction(raw_i) for raw_i in raw_data]
    registers = collections.defaultdict(int)
    # We know the largest value is positive, so zero
    # suffices as small number to seed the 'largest' variable
    largest = 0
    # Execute the loaded instructions
    for instr in instrs:
        instr(registers)
        tmp_max = max(registers.values())
        if tmp_max > largest:
            largest = tmp_max
    # Find the largest value in the registers
    largest_val = max(registers.values())
    print('The largest value is %d' % (largest_val))
    print('The largest value ever was %d' % (largest))


if __name__ == '__main__':
    main(sys.argv)
