from __future__ import annotations
import argparse
import logging
import math
from collections import defaultdict
from copy import deepcopy
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
    return [[int(x) for x in list(line)]
            for line in [line.strip() for line in fp]]


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
        if len(frontier) % 100 == 0:
            logging.debug("Frontier size: %d", len(frontier))
        # Get node with lowest cost
        u = None
        min_dist = math.inf
        for v in frontier:
            if dist[v] < min_dist:
                u = v
                min_dist = dist[v]
        frontier.remove(u)
        if u == (end_x, end_y):
            return dist[u]
        for n_x, n_y in neighbors4(graph, u[0], u[1]):
            # alt = dist[u] + int(graph[n_y][n_x])
            alt = dist[u] + graph[n_y][n_x]
            if alt < dist[(n_x, n_y)]:
                dist[(n_x, n_y)] = alt
                prev[(n_x, n_y)] = u
    return dist[(end_x, end_y)]


def puzzle1(data) -> int:
    start = 0, 0
    end = len(data[0]) - 1, len(data) - 1
    logging.debug("Starting search to %r", end)
    risk = dijkstra(data, start[0], start[1], end[0], end[1])
    return risk


def increment_grid(grid: list[list[int]]):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            grid[y][x] += 1
            if grid[y][x] > 9:
                grid[y][x] = 1
    return grid


def make5by5(grid: list[list[int]]):
    result = deepcopy(grid)
    orig_height = len(grid)
    orig_width = len(grid[0])
    for i in range(4):
        grid = increment_grid(grid)
        for y in range(len(result)):
            result[y].extend(grid[y])
    # Now extend vertically
    for i in range(4):
        # Copy a new set of rows in, offsetting by the original grid
        grid = increment_grid(grid)
        for y in range(orig_height):
            result.append(result[i * orig_height + y][orig_width:]
                          + grid[y])
    return result


def infinity():
    return math.inf


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    return total_path


def A_star(grid, start: tuple[int, int], goal: tuple[int, int], h) -> int:
    open_set = {start}
    came_from = {}
    g_score = defaultdict(infinity)
    g_score[start] = 0
    f_score = defaultdict(infinity)
    f_score[start] = h(start)
    while open_set:
        #  current := the node in openSet having the lowest fScore[] value
        current = None
        current_score = math.inf
        for v in open_set:
            if f_score[v] < current_score:
                current = v
                current_score = f_score[v]
        if current == goal:
            # return reconstruct_path(came_from, current)
            # We just want the score of the path to the goal
            return int(current_score)
        open_set.remove(current)
        for neighbor in neighbors4(grid, current[0], current[1]):
            tentative_g_score = g_score[current] + grid[neighbor[0]][neighbor[1]]
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor)
                if neighbor not in open_set:
                    open_set.add(neighbor)
    raise Exception("Open set is empty but goal was never reached")


def puzzle2(data) -> int:
    grid = make5by5(data)
    # grid = data
    # for y in range(len(grid)):
    #     print(''.join([str(c) for c in grid[y]]))
    start = 0, 0
    end = len(grid[0]) - 1, len(grid) - 1

    # A-star heuristic function
    def h(n: tuple[int, int]) -> int:
        return end[0] - n[0] + end[1] - n[1]

    logging.debug("Starting search to %r", end)
    risk = A_star(grid, start, end, h)
    return risk


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
