import unittest

from day22 import Cube


class TestDay22(unittest.TestCase):

    def test_cube_contains(self):
        c1 = Cube(0, 10, 0, 10, 0, 10)
        c2 = Cube(2, 8, 2, 8, 2, 8)
        self.assertTrue(c1.contains(c2))
        self.assertFalse(c2.contains(c1))
        c3 = Cube(3, 12, 3, 12, 3, 12)
        self.assertFalse(c1.contains(c3))
        self.assertFalse(c3.contains(c1))


if __name__ == '__main__':
    unittest.main()
