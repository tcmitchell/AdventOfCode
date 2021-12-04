from __future__ import annotations
import logging


class BingoBoard:
    BOARD_SIZE = 5

    def __init__(self, board: list[list[int]]) -> None:
        self._board = board
        self._markers = None
        self.clear()

    @staticmethod
    def MakeBoard(data: list[str]):
        assert len(data) == BingoBoard.BOARD_SIZE
        data = [row.split() for row in data]
        data2 = []
        for d in data:
            data2.append([int(x) for x in d])
        logging.debug("data2: %r", data2)
        return BingoBoard(data2)

    def clear(self):
        self._markers = [[0 for r in range(BingoBoard.BOARD_SIZE)]
                         for c in range(BingoBoard.BOARD_SIZE)]

    def mark(self, number: int):
        for r in range(BingoBoard.BOARD_SIZE):
            for c in range(BingoBoard.BOARD_SIZE):
                if self._board[r][c] == number:
                    self._markers[r][c] = 1

    def winner(self) -> bool:
        for r in self._markers:
            if sum(r) == BingoBoard.BOARD_SIZE:
                return True
        for c in range(BingoBoard.BOARD_SIZE):
            if sum([r[c] for r in self._markers]) == BingoBoard.BOARD_SIZE:
                return True
        return False

    def unmarked(self) -> list[int]:
        result = []
        for r in range(BingoBoard.BOARD_SIZE):
            for c in range(BingoBoard.BOARD_SIZE):
                if self._markers[r][c] == 0:
                    result.append(self._board[r][c])
        return result
