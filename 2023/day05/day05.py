from __future__ import annotations
import argparse
import logging
import math
import re
from typing import TextIO, Optional


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


class AlmanacMapEntry:

    def __init__(self, dst_start: int, src_start: int, range_len: int):
        self.dst_start = dst_start
        self.src_start = src_start
        self.range_len = range_len

    def __contains__(self, item: int):
        return self.src_start <= item < self.src_start + self.range_len

    def map(self, item: int) -> int:
        return item - self.src_start + self.dst_start


class AlmanacMap:

    def __init__(self, src: str, dest: str):
        self.source = src
        self.destination = dest
        self.entries: list[AlmanacMapEntry] = []

    def add_entry(self, dst_start, src_start, range_len):
        self.entries.append(AlmanacMapEntry(dst_start, src_start, range_len))

    def lookup(self, value: int):
        for entry in self.entries:
            if value in entry:
                return entry.map(value)
        # No mapping for value, so return the value per the rules
        return value


SEEDS_RE = re.compile(r"seeds:([\s\d]*)")
ALL_NUMBERS_RE = re.compile(r"\d+")

# seed-to-soil map:
MAP_HEADER_RE = re.compile(r"(\w+)-to-(\w+)\s+map:")
MAP_ENTRY_RE = re.compile(r"(\d+)\s+(\d+)\s+(\d+)")

def load_input(fp: TextIO):
    maps = []
    current_map: Optional[AlmanacMap] = None
    # Read the list of seeds
    match = SEEDS_RE.match(fp.readline())
    seeds = [int(n) for n in ALL_NUMBERS_RE.findall(match.group(0))]
    # Now load the maps
    for line in fp:
        line = line.strip()
        if not line:
            # Skip blank lines
            continue
        match = MAP_HEADER_RE.match(line)
        if match is not None:
            current_map = AlmanacMap(match.group(1), match.group(2))
            maps.append(current_map)
            continue
        match = MAP_ENTRY_RE.match(line)
        if match is not None:
            current_map.add_entry(*[int(n) for n in ALL_NUMBERS_RE.findall(line)])
    return seeds, maps


def lookup_location(seed: int, maps: dict[str, AlmanacMap]):
    entry_type = 'seed'
    entry_value = seed
    while entry_type != 'location':
        logging.debug("Mapping %s %d", entry_type, entry_value)
        map = maps[entry_type]
        next_value = map.lookup(entry_value)
        logging.debug("%s %d -> %s %d", entry_type, entry_value, map.destination, next_value)
        entry_type, entry_value = map.destination, next_value
    return entry_value

def puzzle1(data) -> int:
    seeds, maps = data
    map_lookup = {map.source: map for map in maps}
    min_location = math.inf
    for seed in seeds:
        location = lookup_location(seed, map_lookup)
        if location < min_location:
            min_location = location
    return min_location


def puzzle2(data) -> int:
    return 0


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
