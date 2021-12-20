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


class Point3D:

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"<Point3D {(self.x, self.y, self.z)}>"

    def distance(self, other: Point3D):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2


class Scanner:

    def __init__(self, name: str, points: list[Point3D]):
        self.name = name
        self.points = points
        self.distances: dict[Point3D, set[int]] = defaultdict(set)
        self.overlapping_beacons: set[Point3D] = set()

    def __str__(self):
        return f"<Scanner {self.name}>"

    def compute_distances(self):
        # For each point, compute a set of distances to all other points
        for i in range(len(self.points)):
            p1 = self.points[i]
            for j in range(i + 1, len(self.points)):
                p2 = self.points[j]
                dist = p1.distance(p2)
                self.distances[p1].add(dist)
                self.distances[p2].add(dist)


def load_input(fp: TextIO) -> list[Scanner]:
    data = fp.read()
    result: list[Scanner] = []
    for chunk in data.split('\n\n'):
        # print(chunk)
        lines = chunk.strip().split('\n')
        name = lines[0].replace('---', '').strip()
        logging.debug("Handling %s", name)
        points = [Point3D(*[int(x) for x in line.split(',')]) for line in lines[1:]]
        result.append(Scanner(name, points))
    return result


def puzzle1(data: list[Scanner]) -> int:
    num_scanners = len(data)
    # compute distances between all scanned beacons in each scanner
    for s in data:
        s.compute_distances()
    for i in range(num_scanners):
        s1 = data[i]
        for j in range(i + 1, num_scanners):
            s2 = data[j]
            logging.debug("Comparing %s and %s", s1, s2)
            for p1 in s1.points:
                d1 = s1.distances[p1]
                for p2 in s2.points:
                    d2 = s2.distances[p2]
                    overlap = d1.intersection(d2)
                    if len(overlap) >= 11:
                        logging.debug("Intersection of %s and %s = %d", p1, p2, len(overlap))
                        s1.overlapping_beacons.add(p1)
                        s2.overlapping_beacons.add(p2)
    distinct = 0
    for s in data:
        logging.debug("Scanner %s has %d overlapping and %d total beacons",
                      s, len(s.overlapping_beacons), len(s.points))
        distinct += len(s.points) - len(s.overlapping_beacons)
    overlapping_beacons = sum([len(s.overlapping_beacons) for s in data])
    return len(data)


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
