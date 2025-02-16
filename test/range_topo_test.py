import unittest
from random import randint

from src.base_calc import to_number
from src.range_optimization_nonrestricted import crange



class HandpickedTopoTests(unittest.TestCase):
    def test_only_one_path(self):
        l = []
        r = crange(0, 10000, 113, 10, l)
        s = set()
        r.used(s)
        self.assertEqual(len(l), len(s))


if __name__ == '__main__':
    unittest.main()
