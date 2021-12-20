import unittest

from day19 import Point3D


class MyTestCase(unittest.TestCase):

    def test_distance(self):
        p1 = Point3D(0, 0, 0)
        p2 = Point3D(10, 10, 10)
        d = p1.distance(p2)
        # This is really distance squared, it's cheaper than doing lots
        # of square roots
        self.assertEqual(300, d)


if __name__ == '__main__':
    unittest.main()
