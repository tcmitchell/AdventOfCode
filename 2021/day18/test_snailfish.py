import unittest

from node import *


class TestSnailFish(unittest.TestCase):
    """[[1,2],3]
    [9,[8,7]]
    [[1,9],[8,5]]
    [[[[1,2],[3,4]],[[5,6],[7,8]]],9]
    [[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
    [[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]
    """

    def test_parse1(self):
        snum = "[1,2]"
        tree = Pair.parse(snum)
        self.assertIsInstance(tree, Pair)
        self.assertIsInstance(tree.left, Literal)
        self.assertEqual(1, tree.left.value)
        self.assertIsInstance(tree.right, Literal)
        self.assertEqual(2, tree.right.value)
        self.assertEqual(snum, str(tree))

    def test_parse2(self):
        snum = "[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"
        tree = Pair.parse(snum)
        self.assertIsInstance(tree, Pair)
        self.assertIsInstance(tree.left, Pair)
        self.assertIsInstance(tree.right, Pair)
        self.assertEqual(snum, str(tree))

    def test_explode1(self):
        snum = "[[[[[9,8],1],2],3],4]"
        output = "[[[[0,9],2],3],4]"
        tree = Pair.parse(snum)
        self.assertTrue(tree.explode())
        self.assertEqual(output, str(tree))

    def test_explode2(self):
        snum = "[7,[6,[5,[4,[3,2]]]]]"
        output = "[7,[6,[5,[7,0]]]]"
        tree = Pair.parse(snum)
        self.assertTrue(tree.explode())
        self.assertEqual(output, str(tree))

    def test_explode3(self):
        snum = "[[6,[5,[4,[3,2]]]],1]"
        output = "[[6,[5,[7,0]]],3]"
        tree = Pair.parse(snum)
        self.assertTrue(tree.explode())
        self.assertEqual(output, str(tree))

    def test_explode4(self):
        snum = "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]"
        output = "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
        tree = Pair.parse(snum)
        self.assertTrue(tree.explode())
        self.assertEqual(output, str(tree))

    def test_explode5(self):
        snum = "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
        output = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
        tree = Pair.parse(snum)
        self.assertTrue(tree.explode())
        self.assertEqual(output, str(tree))

    def test_explode_nothing(self):
        snum = "[[1,2],3]"
        tree = Pair.parse(snum)
        self.assertFalse(tree.explode())

    def test_split_nothing(self):
        snum = "[[1,2],3]"
        tree = Pair.parse(snum)
        self.assertFalse(tree.split())

    def test_split1(self):
        snum = "[[[[0,7],4],[15,[0,13]]],[1,1]]"
        output = "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
        tree = Pair.parse(snum)
        self.assertTrue(tree.split())
        self.assertEqual(output, str(tree))

    def test_split2(self):
        snum = "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]"
        output = "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]"
        tree = Pair.parse(snum)
        self.assertTrue(tree.split())
        self.assertEqual(output, str(tree))

    def test_reduce1(self):
        snum = "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"
        output = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
        tree = Pair.parse(snum)
        tree.reduce()
        self.assertEqual(output, str(tree))

    def test_add(self):
        snum1 = "[[[[4,3],4],4],[7,[[8,4],9]]]"
        snum2 = "[1,1]"
        output = "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
        tree1 = Pair.parse(snum1)
        tree2 = Pair.parse(snum2)
        tree = tree1.add(tree2)
        self.assertEqual(output, str(tree))



if __name__ == '__main__':
    unittest.main()
