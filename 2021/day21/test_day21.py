import unittest

from day21 import DeterministicDice


class TestDay21(unittest.TestCase):

    def test_roll3(self):
        dd = DeterministicDice(100)
        self.assertEqual(6, dd.roll3())
        self.assertEqual(3, dd.rolls)
        self.assertEqual(15, dd.roll3())
        self.assertEqual(6, dd.rolls)
        dd.roll_n(100)
        self.assertEqual(106, dd.rolls)
        self.assertEqual(7, dd.roll())


if __name__ == '__main__':
    unittest.main()
