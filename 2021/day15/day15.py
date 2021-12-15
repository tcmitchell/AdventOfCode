from __future__ import annotations
import argparse
import logging
import math
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


def load_input(fp: TextIO):
    return [line.strip() for line in fp.readlines()]


def neighbors4(grid, x, y) -> list[tuple[int, int]]:
    """Return the horizontal and vertical neighbors of the given
    position on the given grid. This function ignores diagonal
    neighbors.
    """
    max_y = len(grid)
    max_x = len(grid[0])
    result = [(x-1, y), (x, y-1), (x, y+1), (x+1, y)]
    result = [(x, y) for x, y in result if 0 <= x < max_x and 0 <= y < max_y]
    return result


def dijkstra(graph, start_x, start_y, end_x, end_y) -> int:
    # See https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
    dist = {}
    prev = {}
    frontier = set()
    for y in range(len(graph)):
        for x in range(len(graph[0])):
            dist[(x, y)] = math.inf
            prev[(x, y)] = None
            frontier.add((x, y))
    dist[(start_x, start_y)] = 0

    while frontier:
        # Get node with lowest cost
        u = None
        min_dist = math.inf
        for v in frontier:
            if dist[v] < min_dist:
                u = v
                min_dist = dist[v]
        frontier.remove(u)
        # if u == (end_x, end_y):
        #     return dist[u]
        for n_x, n_y in neighbors4(graph, u[0], u[1]):
            alt = dist[u] + int(graph[n_y][n_x])
            if alt < dist[(n_x, n_y)]:
                dist[(n_x, n_y)] = alt
                prev[(n_x, n_y)] = u
    return dist[(end_x, end_y)]


def puzzle1(data) -> int:
    start = 0, 0
    end = len(data[0]) - 1, len(data) - 1
    risk = dijkstra(data, start[0], start[1], end[0], end[1])
    return risk


def puzzle2(data) -> int:
    return 0


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
