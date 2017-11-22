#!/usr/bin/env python

import pprint
import re
import sys

node_prog = re.compile(r'(/dev/grid\S*)\s*\d*T\s*(\d*)T\s*(\d*)T')
#node_prog = re.compile(r'(/dev/grid\S*)')

def load_nodes(infile):
    nodes = []
    with open(infile, 'rb') as f:
        for line in f:
            match = node_prog.match(line)
            if match:
                (name, usage, avail) = match.groups()
                nodes.append((name, int(usage), int(avail)))
    return nodes

def main(argv=None):
    if argv is None:
        argv = sys.argv
    infile = argv[1]
    nodes = load_nodes(infile)
    # pprint.pprint(nodes)
    nodes_by_usage = sorted(nodes, key=lambda x: x[1])
    nodes_by_avail = sorted(nodes, key=lambda x: x[2], reverse=True)
    for i in range(10):
        print 'Usage', nodes_by_usage[i]
    for node in nodes_by_avail:
        print 'Avail', node
    viable = 0
    for source in nodes_by_usage:
        usage = source[1]
        if usage == 0:
            continue
        for dest in nodes_by_avail:
            avail = dest[2]
            if usage <= avail:
                viable += 1
            else:
                break
    print 'Viable pairs:', viable


if __name__ == '__main__':
    main()
