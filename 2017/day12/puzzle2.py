#!/usr/bin/env python3

# http://adventofcode.com/2017/day/12

import sys


def parse_line(input_line):
    tmp = input_line.split(b'<->')
    prog_id = int(tmp[0])
    conns = [int(conn) for conn in tmp[1].split(b',')]
    return (prog_id, conns)


def load_input(datafile):
    with open(datafile, 'rb') as f:
        parsed = [parse_line(l) for l in f.readlines()]
    return {pid: conns for (pid, conns) in parsed}


def main(argv):
    datafile = argv[1]
    data = load_input(datafile)
    groups = []
    connected = []
    disconnected = sorted([k for k in data.keys() if k not in connected])
    while disconnected:
        key0 = disconnected[0]
        group0 = set([key0])
        new = [key0]
        while new:
            new_new = []
            for pid in new:
                for neighbor in data[pid]:
                    if neighbor not in group0:
                        group0.add(neighbor)
                        new_new.append(neighbor)
            new = new_new
        groups.append(group0)
        connected.extend(group0)
        disconnected = sorted([k for k in data.keys() if k not in connected])
    print(len(groups))


if __name__ == '__main__':
    main(sys.argv)
