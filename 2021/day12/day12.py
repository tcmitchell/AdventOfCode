from __future__ import annotations
import argparse
import logging
from collections import defaultdict
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


def load_input(fp: TextIO) -> list[list[str]]:
    return [line.strip().split('-') for line in fp]


def puzzle1(data: list[list[str]]) -> int:
    graph: dict[str, list[str]] = defaultdict(list)
    for pair in data:
        graph[pair[0]].append(pair[1])
        graph[pair[1]].append(pair[0])
    complete_paths = []
    pathq = [['start']]
    while pathq:
        path = pathq.pop(0)
        neighbors = graph[path[-1]]
        for node in neighbors:
            if node.islower() and node in path:
                # lowercase nodes cannot repeat
                continue
            new_path = path.copy()
            new_path.append(node)
            if node == 'end':
                complete_paths.append(new_path)
            else:
                pathq.append(new_path)
    return len(complete_paths)


def has_repeating_lower(path: list[str]):
    # skip 'start'
    for i in range(1, len(path)):
        node = path[i]
        if not node.islower():
            continue
        if node in path[i+1:]:
            return True
    return False


def puzzle2(data: list[list[str]]) -> int:
    graph: dict[str, list[str]] = defaultdict(list)
    for pair in data:
        graph[pair[0]].append(pair[1])
        graph[pair[1]].append(pair[0])
    complete_paths = []
    pathq = [['start']]
    while pathq:
        path = pathq.pop(0)
        neighbors = graph[path[-1]]
        for node in neighbors:
            if node == 'start':
                continue
            if node.islower() and has_repeating_lower(path) and node in path:
                # only one lowercase node can repeat
                continue
            new_path = path.copy()
            new_path.append(node)
            if node == 'end':
                complete_paths.append(new_path)
            else:
                pathq.append(new_path)
    return len(complete_paths)


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    answer = puzzle1(data)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(data)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main()
