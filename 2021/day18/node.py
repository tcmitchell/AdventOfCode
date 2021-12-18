from __future__ import annotations

import logging
import math
from typing import Union, Optional


class Node:

    def __init__(self):
        self.parent: Union[Node, None] = None
        self.left: Union[Node, None] = None
        self.right: Union[Node, None] = None

    def explode(self, depth=0) -> bool:
        return False

    def split(self) -> bool:
        return self.left.split() or self.right.split()

    def reduce(self):
        logging.debug("Starting: %s", self)
        while self.explode() or self.split():
            logging.debug("After: %s", self)
            pass
        logging.debug("Finished: %s", self)

    def all_literals(self) -> list[Literal]:
        return []

    def replace(self, old_node, new_node):
        raise Exception("Not implemented")

    def top(self):
        if self.parent is None:
            return self
        else:
            return self.parent.top()

    def make_pair(self, left: Node, right: Node) -> Node:
        raise Exception("Not implemented")

    def add(self, tree: Node) -> Node:
        pair = Pair(self, tree)
        pair.reduce()
        return pair

    def magnitude(self) -> int:
        raise Exception("Not implemented")


class Literal(Node):

    def __init__(self, value: int):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def all_literals(self) -> list[Literal]:
        return [self]

    def split(self) -> bool:
        if self.value < 10:
            return False
        logging.debug("Need to split %d", self.value)
        new_left = Literal(math.floor(self.value / 2))
        new_right = Literal(math.ceil(self.value / 2))
        new_node = self.parent.make_pair(new_left, new_right)
        self.parent.replace(self, new_node)
        return True

    def magnitude(self) -> int:
        return self.value


class Pair(Node):

    def __init__(self, left: Optional[Node] = None, right: Optional[Node] = None):
        super().__init__()
        self.left = left
        if left is not None:
            left.parent = self
        self.right = right
        if right is not None:
            right.parent = self

    def __str__(self):
        return f"[{str(self.left)},{str(self.right)}]"

    def explode(self, depth=0) -> bool:
        if depth < 4:
            return self.left.explode(depth+1) or self.right.explode(depth+1)
        if not isinstance(self.left, Literal) or not isinstance(self.right, Literal):
            raise Exception("Trying to explode with non-literals")
        all_literals = self.top().all_literals()
        # Add to the left
        left_index = all_literals.index(self.left)
        if left_index > 0:
            left_neighbor = all_literals[left_index - 1]
            left_neighbor.value += self.left.value
        # Add to the right
        right_index = all_literals.index(self.right)
        if right_index < len(all_literals) - 1:
            right_neighbor = all_literals[right_index + 1]
            right_neighbor.value += self.right.value
        self.parent.replace(self, Literal(0))
        return True

    def replace(self, old_node, new_node):
        if self.left == old_node:
            self.left = new_node
            new_node.parent = self
        elif self.right == old_node:
            self.right = new_node
            new_node.parent = self
        else:
            raise Exception("replace on non-existent old_node")

    def all_literals(self) -> list[Literal]:
        return self.left.all_literals() + self.right.all_literals()

    def make_pair(self, left: Node, right: Node) -> Node:
        pair = Pair(left, right)
        return pair

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    @staticmethod
    def parse(snum) -> Node:
        if isinstance(snum, str):
            snum = eval(snum)
        if isinstance(snum, int):
            return Literal(snum)
        pair = Pair()
        pair.left = Pair.parse(snum[0])
        pair.left.parent = pair
        pair.right = Pair.parse(snum[1])
        pair.right.parent = pair
        return pair


def parse_snailfish(number: str):
    num_list = eval(number)
    tree = Pair.parse(num_list)
