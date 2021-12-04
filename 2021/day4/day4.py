from __future__ import annotations
import argparse
import logging
import sys
from typing import TextIO

from bingo import BingoBoard


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


def load_input(fp: TextIO):
    # One line of numbers to call
    # Followed by a series of Bingo Boards
    data = [line.strip() for line in fp.readlines()]
    call_numbers = data[0]
    call_numbers = [int(x) for x in call_numbers.split(',')]
    boards = []
    data = data[1:]
    for d in range(len(data)//6):
        logging.debug(data[1:6])
        boards.append(BingoBoard.MakeBoard(data[1:6]))
        data = data[6:]
    return call_numbers, boards


def puzzle1(call_numbers: list[int], boards: list[BingoBoard]) -> int:
    for cn in call_numbers:
        for board in boards:
            board.mark(cn)
            if board.winner():
                logging.info("Winner!")
                unmarked = board.unmarked()
                sum_unmarked = sum(unmarked)
                return sum_unmarked * cn
    return 0


def puzzle2(call_numbers: list[int], boards: list[BingoBoard]) -> int:
    for cn in call_numbers:
        for board in boards:
            board.mark(cn)
        # filter winning boards
        losers = [b for b in boards if not b.winner()]
        if losers:
            boards = losers
            continue
        else:
            # No more boards!
            logging.info("One non-winner")
            board = boards[0]
            unmarked = board.unmarked()
            sum_unmarked = sum(unmarked)
            return sum_unmarked * cn
    return 0


def main(argv):
    if not argv:
        argv = sys.argv
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    call_numbers, boards = load_input(args.input)
    answer = puzzle1(call_numbers, boards)
    logging.info('Puzzle 1: %d', answer)
    answer = puzzle2(call_numbers, boards)
    logging.info('Puzzle 2: %d', answer)


if __name__ == '__main__':
    main(sys.argv)
