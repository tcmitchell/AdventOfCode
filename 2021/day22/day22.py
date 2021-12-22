from __future__ import annotations
import argparse
import logging
import re
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


def load_input(fp: TextIO):
    result = []
    for line in fp:
        verb, rest = line.strip().split()
        dims = [int(x) for x in re.findall(r'-?\d+', rest)]
        result.append((verb, dims))
    return result


class Cube:

    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2
        self.z1, self.z2 = z1, z2

    def __repr__(self):
        return f"Cube({self.x1}, {self.x2}, {self.y1}, {self.y2}, {self.z1}, {self.z2})"

    def volume(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1) * (self.z2 - self.z1)

    def contains(self, other: Cube) -> bool:
        """True if other is fully contained in self."""
        return (self.x1 <= other.x1 and self.x2 >= other.x2
                and self.y1 <= other.y1 and self.y2 >= other.y2
                and self.z1 <= other.z1 and self.z2 >= other.z2)

    def overlaps(self, other: Cube) -> bool:
        """True if this cube overlaps with other in any way."""
        # See https://silentmatt.com/rectangle-intersection/
        return (self.x1 <= other.x2 and self.x2 >= other.x1
                and self.y1 <= other.y2 and self.y2 >= other.y1
                and self.z1 <= other.z2 and self.z2 >= other.z1)

    def subcubes(self, other: Cube) -> list[Cube]:
        """Return a list of cubes representing the parts of self that
        do not overlap `other`.
        """
        if other.contains(self):
            # There are no overlapping parts
            return []
        if not self.overlaps(other):
            # The cubes do not overlap, so no sub-cubes
            return [self]

        # Credit here to https://github.com/mebeim
        x_coords = [self.x1]
        if self.x1 < other.x1 < self.x2:
            x_coords.append(other.x1)
        if self.x1 < other.x2 < self.x2:
            x_coords.append(other.x2)
        x_coords.append(self.x2)

        y_coords = [self.y1]
        if self.y1 < other.y1 < self.y2:
            y_coords.append(other.y1)
        if self.y1 < other.y2 < self.y2:
            y_coords.append(other.y2)
        y_coords.append(self.y2)

        z_coords = [self.z1]
        if self.z1 < other.z1 < self.z2:
            z_coords.append(other.z1)
        if self.z1 < other.z2 < self.z2:
            z_coords.append(other.z2)
        z_coords.append(self.z2)

        result = []
        for xfrom, xto in zip(x_coords, x_coords[1:]):
            for yfrom, yto in zip(y_coords, y_coords[1:]):
                for zfrom, zto in zip(z_coords, z_coords[1:]):
                    subcube = Cube(xfrom, xto, yfrom, yto, zfrom, zto)
                    if other.contains(subcube) or subcube.volume() <= 0:
                        continue
                    result.append(subcube)
        return result


def do_step1(reactor, verb, dims):
    x1, x2, y1, y2, z1, z2 = dims
    setting = verb == 'on'
    for x in range(x1, x2 + 1):
        if x < -50 or x > 50:
            continue
        for y in range(y1, y2 + 1):
            if y < -50 or y > 50:
                continue
            for z in range(z1, z2 + 1):
                if z < -50 or z > 50:
                    continue
                reactor[(x, y, z)] = setting


def puzzle1(steps) -> int:
    reactor = defaultdict(bool)
    for verb, dims in steps:
        do_step1(reactor, verb, dims)
    count_on = len([v for v in reactor.values() if v])
    return count_on


def do_step2(reactor, verb, dims):
    x1, x2, y1, y2, z1, z2 = dims
    setting = verb == 'on'
    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            for z in range(z1, z2 + 1):
                reactor[(x, y, z)] = setting


def puzzle2(steps) -> int:
    cubes = []
    for verb, dims in steps:
        x1, x2, y1, y2, z1, z2 = dims
        cube = Cube(x1, x2 + 1, y1, y2 + 1, z1, z2 + 1)
        new_cubes = []
        for other in cubes:
            new_cubes.extend(other.subcubes(cube))
        if verb == 'on':
            new_cubes.append(cube)
        cubes = new_cubes
    return sum(c.volume() for c in cubes)


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
