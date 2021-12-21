from __future__ import annotations
import argparse
import logging
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


class DeterministicDice:

    def __init__(self, sides: int):
        self.sides = sides
        self.rolls = 0

    def roll(self):
        """Rolls the dice and returns the result"""
        self.rolls += 1
        return self.rolls % self.sides

    def roll_n(self, n: int) -> int:
        """Rolls the dice N times and returns the sum of the rolls"""
        return sum([self.roll() for _ in range(n)])

    def roll3(self):
        """Rolls the dice 3 times and returns the sum of the rolls"""
        return self.roll_n(3)


class Player:

    def __init__(self, name: str, position: int):
        self.name = name
        self.position = position
        self.score = 0

    def __repr__(self):
        return f"<Player {self.name}: p={self.position} s={self.score}>"

    def take_turn(self, dd: DeterministicDice):
        moves = dd.roll3()
        new_position = (self.position + moves - 1) % 10 + 1
        self.position = new_position
        self.score += self.position


def load_input(fp: TextIO) -> list[Player]:
    lines = fp.readlines()
    info = [line.strip().split(' starting position: ') for line in lines]
    return [Player(d[0], int(d[1])) for d in info]


def play_game(players: list[Player], dd: DeterministicDice, win_score: int):
    while True:
        for p in players:
            p.take_turn(dd)
            if p.score >= win_score:
                logging.debug("Winner = %s", p.name)
                return p


def puzzle1(players: list[Player]) -> int:
    dd = DeterministicDice(100)
    winner = play_game(players, dd, 1000)
    for p in players:
        if p == winner:
            continue
        return p.score * dd.rolls
    return 0


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
