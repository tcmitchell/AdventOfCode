import argparse
import collections
import datetime
import itertools
import logging
import re
import sys
import time

# Wrong: 64,86 -- did not sort cars
# Right: 64,57


class Car:

    NORTH = '^'
    SOUTH = 'v'
    WEST = '<'
    EAST = '>'
    DIRECTIONS = [NORTH, SOUTH, EAST, WEST]
    LEFT = 1
    STRAIGHT = 2
    RIGHT = 3

    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.next_turn = Car.LEFT
        if self.direction in [Car.NORTH, Car.SOUTH]:
            self.track_segment = '|'
        if self.direction in [Car.EAST, Car.WEST]:
            self.track_segment = '-'

    def tick(self, tracks):
        if self.direction == Car.EAST:
            self.move_east(tracks)
        elif self.direction == Car.SOUTH:
            self.move_south(tracks)
        elif self.direction == Car.NORTH:
            self.move_north(tracks)
        elif self.direction == Car.WEST:
            self.move_west(tracks)
        else:
            raise Exception('Unknown direction {}'.format(self.direction))

    def move_east(self, tracks):
        next_x = self.x + 1
        if tracks[self.y][next_x] in Car.DIRECTIONS:
            raise Exception('Crash detected at {},{}'.format(next_x, self.y))
        elif tracks[self.y][next_x] == '\\':
            self.direction = Car.SOUTH
        elif tracks[self.y][next_x] == '/':
            self.direction = Car.NORTH
        elif tracks[self.y][next_x] == '+':
            if self.next_turn == Car.LEFT:
                logging.debug('Turning Left')
                self.direction = Car.NORTH
                self.next_turn = Car.STRAIGHT
            elif self.next_turn == Car.STRAIGHT:
                logging.debug('Going Straight')
                self.next_turn = Car.RIGHT
            elif self.next_turn == Car.RIGHT:
                logging.debug('Turning Right')
                self.direction = Car.SOUTH
                self.next_turn = Car.LEFT
        # Remove self from the track momentarily
        tracks[self.y][self.x] = self.track_segment
        self.x = next_x
        self.track_segment = tracks[self.y][self.x]
        tracks[self.y][self.x] = self.direction

    def move_west(self, tracks):
        next_x = self.x - 1
        if tracks[self.y][next_x] in Car.DIRECTIONS:
            raise Exception('Crash detected at {},{}'.format(next_x, self.y))
        elif tracks[self.y][next_x] == '\\':
            self.direction = Car.NORTH
        elif tracks[self.y][next_x] == '/':
            self.direction = Car.SOUTH
        elif tracks[self.y][next_x] == '+':
            if self.next_turn == Car.LEFT:
                self.direction = Car.SOUTH
                self.next_turn = Car.STRAIGHT
            elif self.next_turn == Car.STRAIGHT:
                self.next_turn = Car.RIGHT
            elif self.next_turn == Car.RIGHT:
                self.direction = Car.NORTH
                self.next_turn = Car.LEFT
        # Remove self from the track momentarily
        tracks[self.y][self.x] = self.track_segment
        self.x = next_x
        self.track_segment = tracks[self.y][self.x]
        tracks[self.y][self.x] = self.direction

    def move_south(self, tracks):
        next_y = self.y + 1
        if tracks[next_y][self.x] in Car.DIRECTIONS:
            raise Exception('Crash detected at {},{}'.format(self.x, next_y))
        elif tracks[next_y][self.x] == '\\':
            self.direction = Car.EAST
        elif tracks[next_y][self.x] == '/':
            self.direction = Car.WEST
        elif tracks[next_y][self.x] == '+':
            if self.next_turn == Car.LEFT:
                self.direction = Car.EAST
                self.next_turn = Car.STRAIGHT
            elif self.next_turn == Car.STRAIGHT:
                self.next_turn = Car.RIGHT
            elif self.next_turn == Car.RIGHT:
                self.direction = Car.WEST
                self.next_turn = Car.LEFT
        # Remove self from the track momentarily
        tracks[self.y][self.x] = self.track_segment
        self.y = next_y
        self.track_segment = tracks[self.y][self.x]
        tracks[self.y][self.x] = self.direction

    def move_north(self, tracks):
        next_y = self.y - 1
        if tracks[next_y][self.x] in Car.DIRECTIONS:
            raise Exception('Crash detected at {},{}'.format(self.x, next_y))
        elif tracks[next_y][self.x] == '\\':
            self.direction = Car.WEST
        elif tracks[next_y][self.x] == '/':
            self.direction = Car.EAST
        elif tracks[next_y][self.x] == '+':
            if self.next_turn == Car.LEFT:
                self.direction = Car.WEST
                self.next_turn = Car.STRAIGHT
            elif self.next_turn == Car.STRAIGHT:
                self.next_turn = Car.RIGHT
            elif self.next_turn == Car.RIGHT:
                self.direction = Car.EAST
                self.next_turn = Car.LEFT
        # Remove self from the track momentarily
        tracks[self.y][self.x] = self.track_segment
        self.y = next_y
        self.track_segment = tracks[self.y][self.x]
        tracks[self.y][self.x] = self.direction


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=argparse.FileType('r'),
                        metavar="PUZZLE_INPUT")
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()
    return args


def init_logging(debug=False):
    msgFormat = '%(asctime)s %(levelname)s %(message)s'
    dateFormat = '%m/%d/%Y %H:%M:%S'
    level = logging.INFO
    if debug:
        level = logging.DEBUG
    logging.basicConfig(format=msgFormat, datefmt=dateFormat, level=level)


def load_input(fp):
    return [list(line.strip('\n')) for line in fp]


def parse_tracks(tracks):
    cars = []
    for y in range(len(tracks)):
        data = list(tracks[y])
        for x in range(len(data)):
            if data[x] in [Car.NORTH, Car.SOUTH]:
                cars.append(Car(x, y, data[x]))
            elif data[x] in [Car.EAST, Car.WEST]:
                cars.append(Car(x, y, data[x]))
    return tracks, cars


def print_tracks(tracks):
    for row in tracks:
        print(''.join(row))


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    tracks = load_input(args.input)
    tracks, cars = parse_tracks(tracks)
    print_tracks(tracks)
    logging.info('There are {} cars'.format(len(cars)))

    tick = 0
    for i in range(200):
        for c in cars:
            c.tick(tracks)
        tick += 1
        logging.info('After {} ticks:'.format(tick))
        cars.sort(key=lambda c: (c.y, c.x))
        # print_tracks(tracks)


if __name__ == '__main__':
    main(sys.argv)
