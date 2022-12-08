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


class Directory:

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.size = None

    def __repr__(self):
        return f'<Directory {self.name}>'

    def add_child(self, child):
        self.children[child.name] = child

    def get_child(self, name: str):
        return self.children[name]

    def compute_size(self) -> int:
        if self.size is None:
            self.size = sum([child.compute_size() for child in self.children.values()])
        return self.size

    def visit(self, visitor):
        visitor.visit_directory(self)


class File:

    def __init__(self, name: str, size: int, parent: Directory):
        self.name = name
        self.size = size
        self.parent = parent

    def __repr__(self):
        return f'<File {self.name}>'

    def compute_size(self) -> int:
        return self.size

    def visit(self, visitor):
        visitor.visit_file(self)


class SizeVisitor:

    def __init__(self):
        self.dirs = []

    def visit_directory(self, directory):
        if directory.compute_size() <= 100000:
            self.dirs.append(directory)
        for child in directory.children.values():
            child.visit(self)

    def visit_file(self, file):
        pass


class AllVisitor:

    def __init__(self, needed):
        self.best_dir = None
        self.needed = needed

    def visit_directory(self, directory):
        if directory.compute_size() > self.needed:
            if self.best_dir is None:
                self.best_dir = directory
            elif directory.compute_size() < self.best_dir.compute_size():
                self.best_dir = directory
        for child in directory.children.values():
            child.visit(self)

    def visit_file(self, file):
        pass


def load_input(fp: TextIO):
    return [line.strip() for line in fp.readlines()]


def parse_data(data: list[str]):
    root = Directory('root')
    root.add_child(Directory('/'))
    cur_dir = root
    while data:
        line = data.pop(0)
        if line.startswith('$'):
            if line.startswith('$ cd '):
                print(line)
                dir_name = line[5:]
                if dir_name == '..':
                    cur_dir = cur_dir.parent
                    print(f'Now in {cur_dir.name}')
                    continue
                cur_dir = cur_dir.get_child(dir_name)
                print(f'Now in {cur_dir.name}')
            if line == '$ ls':
                pass
        elif line.startswith('dir'):
            dir_name = line[4:]
            child_dir = Directory(dir_name, cur_dir)
            cur_dir.add_child(child_dir)
        else:
            str_size, file_name = line.split()
            new_file = File(file_name, int(str_size), cur_dir)
            cur_dir.add_child(new_file)
    return root


def puzzle1(data: list[str]) -> tuple[Directory, int]:
    root = parse_data(data)
    # Compute and cache all sizes
    root.compute_size()
    visitor = SizeVisitor()
    root.get_child('/').visit(visitor)
    return root, sum([x.compute_size() for x in visitor.dirs])


def puzzle2(root: Directory) -> int:
    available = 70000000
    required = 30000000
    used = root.compute_size()
    free = available - used
    needed = required - free
    visitor = AllVisitor(needed)
    root.get_child('/').visit(visitor)
    return visitor.best_dir.compute_size()


def main(argv=None):
    args = parse_args(argv)

    # Init logging
    init_logging(args.debug)

    data = load_input(args.input)
    root, answer = puzzle1(data)
    logging.info('Puzzle 1: %r', answer)
    answer = puzzle2(root)
    logging.info('Puzzle 2: %r', answer)


if __name__ == '__main__':
    main()
