import unittest

from src.base_calc import numberToBase, to_number


class MyTestCase(unittest.TestCase):
    def test_number_to_base(self):
        self.assertEqual([1, 3, 2, 4], numberToBase(1324, 10))

        self.assertEqual([0], numberToBase(0, 5))

        self.assertEqual([1, 0, 1, 0], numberToBase(10, 2))

        self.assertEqual([1234], numberToBase(1234, 1))

        n = 94210
        self.assertEqual("0b" + "".join(map(str, numberToBase(n, 2))), bin(n))

    def test_to_number(self):
        self.assertEqual(1324, to_number([1, 3, 2, 4], 10))

        self.assertEqual(0, to_number([0], 5))

        self.assertEqual(10, to_number([1, 0, 1, 0], 2))

        self.assertEqual(1234, to_number([1234], 1))

        n = 94210
        self.assertEqual(to_number([k == "1" for k in bin(n)[2:]], 2), n)


if __name__ == '__main__':
    unittest.main()
