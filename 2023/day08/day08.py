from __future__ import annotations
import argparse
import itertools
import logging
import math
import re
from typing import TextIO


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType('r'),
                        metavar="PUZZLE_INPUT")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args(args)
    return args


def init_logging(debug=False):
    msg_format = '%(asctime)s %(levelname)s %(message)s'
    date_format = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msg_format, datefmt=date_format, level=level)


ALL_TOKENS_RE = re.compile("\w+")


def load_input(fp: TextIO) -> tuple[str, dict[str, list[str]]]:
    turns = fp.readline().strip()
    # Skip blank line
    fp.readline()
    # Read node data
    data = {}
    for line in fp:
        tokens = ALL_TOKENS_RE.findall(line)
        data[tokens[0]] = [tokens[1], tokens[2]]
    return turns, data


def turns_to_indices(turns: str) -> list[int]:
    turns = turns.replace('L', '0')
    turns = turns.replace('R', '1')
    return [int(t) for t in turns]


def puzzle1(data: tuple[str, dict[str, list[str]]]) -> int:
    turns, nodes = data
    turn = itertools.cycle(turns_to_indices(turns))
    cur_node = 'AAA'
    end_node = 'ZZZ'
    steps = 0
    while cur_node != end_node:
        cur_node = nodes[cur_node][next(turn)]
        steps += 1
    return steps

def puzzle2(data) -> int:
    turns, all_nodes = data
    # Find all start nodes
    start_nodes = [n for n in all_nodes.keys() if n.endswith('A')]
    # Compute steps for each node to get to an end node, then
    # use least common multiple to determine the total steps.
    # Iterating to the end one by one takes too long
    node_steps = []
    for node in start_nodes:
        steps = 0
        turn = itertools.cycle(turns_to_indices(turns))
        while not node.endswith('Z'):
            node = all_nodes[node][next(turn)]
            steps += 1
        node_steps.append(steps)
    logging.debug("%r", node_steps)
    return math.lcm(*node_steps)


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(data)
    logging.info('Puzzle 1: %r', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %r', answer)


if __name__ == '__main__':
    main()
