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


def load_input(fp: TextIO):
    return fp.read().strip()


def input_to_disk(data: str) -> list[str]:
    disk = []
    file_id = 0
    for i in range(0, len(data), 2):
        disk.extend([f"{file_id}"] * int(data[i]))
        try:
            disk.extend(["."] * int(data[i + 1]))
        except IndexError:
            # we've run off the end of the data, which is fine
            pass
        file_id += 1
    return disk


def defrag1(disk: list[str]) -> list[str]:
    free_ptr = disk.index(".")
    file_ptr = len(disk) - 1
    while free_ptr < file_ptr:
        # find the last file block
        while disk[file_ptr] == ".":
            file_ptr -= 1
        disk[free_ptr], disk[file_ptr] = disk[file_ptr], disk[free_ptr]
        while disk[free_ptr] != ".":
            free_ptr += 1
    return disk


def checksum1(disk: list[str]) -> int:
    checksum = 0
    for pos in range(len(disk)):
        try:
            checksum += pos * int(disk[pos])
        except ValueError:
            continue
    return checksum


def puzzle1(data: str) -> int:
    disk = input_to_disk(data)
    # print("".join(disk))
    disk = defrag1(disk)
    # print("".join(disk))
    return checksum1(disk)


def rfind_file(disk: list[str], start: int) -> tuple[int, int]:
    ptr = start
    while disk[ptr] == ".":
        ptr -= 1
    file_id = disk[ptr]
    file_size = 1
    while disk[ptr] == file_id:
        ptr -= 1
        file_size += 1
    return ptr + 1, file_size - 1


def find_free_block(disk: list[str], start: int, size: int) -> int:
    ptr = start
    free_block = ["."] * size
    while ptr < len(disk):
        if disk[ptr: ptr + size ] == free_block:
            return ptr
        ptr += 1
    return -1


def defrag2(disk: list[str]) -> list[str]:
    logger = logging.getLogger("puzzle2")
    file_ptr = len(disk) - 1
    while file_ptr > 0:
        file_ptr, file_size = rfind_file(disk, file_ptr)
        logger.debug("file_ptr = %d, file_size = %d (%s)", file_ptr, file_size, disk[file_ptr:file_ptr + file_size])
        free_ptr = find_free_block(disk, disk.index("."), file_size)
        if 0 <= free_ptr < file_ptr:
            disk[free_ptr:free_ptr + file_size], disk[file_ptr: file_ptr + file_size] = disk[file_ptr: file_ptr + file_size], disk[free_ptr:free_ptr + file_size]
            # print("".join(disk))
        else:
            # Skip this file
            file_ptr -= 1
    return disk


def puzzle2(data) -> int:
    disk = input_to_disk(data)
    # print("".join(disk))
    disk = defrag2(disk)
    return checksum1(disk)


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
