import unittest
from random import randint
from typing import Tuple, Any

from src.base_calc import numberToBase, order
from src.range_optimization_nonrestricted import crange, to_number_special


def compare_range_fast(start, stop, step, base, debug = False) -> tuple[Any, Any, Any, Any] | None:
    if debug: print(start, stop, step, base)
    reference = range(start, stop, step)
    rn, l = crange(start, stop, step, base)

    matching = True
    k = 0
    o = order(step, base)
    # numbers is wrong still
    for n in rn.numbers(base, len(numberToBase(stop, base)) - 1 + o):
        at_p = n in reference
        if debug and not at_p: print(f"path_{k} {p} not included")
        matching = matching and at_p
        k += 1

    if debug and k != len(reference): print(f"number of paths {k} (expected {len(reference)})")
    if matching and len(reference) == k:
        return None
    else:
        return (start, stop, step, base)

def compare_range(start, stop, step, base) -> tuple[Any, Any, Any, Any] | None:
    # print(start, stop, step, base)
    rn, l = crange(start, stop, step, base)

    wanted_range = list(range(start, stop, step))
    o = order(step, base)
    opt_range = [to_number_special(i, o, base) for i in rn.paths()]
    opt_range.sort()

    if wanted_range == opt_range:
        return None
    else:
        return (start, stop, step, base)

def compare_ranges(args) -> list[tuple]:
    return [a for a in args if not compare_range(*a)]

def compare_ranges_fast(args) -> list[tuple]:
    ret = []
    for a in args:
        r = compare_range_fast(*a)
        if r is not None:
            ret.append(r)
    return ret

from multiprocessing import Pool

# def compare_ranges_par(args) -> list[tuple]:
#     p = Pool()
#     res = p.map(lambda a: None if compare_range(*a) else a, args)
#     return [a for a in res if a is not None]

def compare_ranges_par(args) -> list[tuple]:
    p = Pool()
    res = p.starmap(compare_range, args)
    return [a for a in res if a is not None]

class HandpickedTests(unittest.TestCase):
    def test_only_one_path(self):
        tests = [(923, 931, 93, 10),
                 (75, 92, 19, 10)]

        self.assertListEqual([], compare_ranges(tests))

    def test_size_intermediate_layers_edge_case(self):
        tests = [(0, 292815, 8, 10)]   # edge case for size intermediate layers!

        self.assertListEqual([], compare_ranges(tests))

    def test_root_is_one_path(self):
        tests = [(11111, 11112, 3, 10),
                 (123222, 123589, 20, 10),
                 (9999095, 9999995, 15, 20)]

        self.assertListEqual([], compare_ranges(tests))

    def test_minimal_sequence(self):
        tests = [(1087, 9000, 87, 10),  # minimal_seq(r1)
                 (1087, 9000, 15, 10)]

        self.assertListEqual([], compare_ranges(tests))

    def test_previously_wrong(self):
        tests = [
            (611, 30000, 37, 10),
            (730, 3000, 2, 10),
            (7, 3000, 69, 10),
            (312, 15000, 15, 10),
            (10, 15, 5, 10),
            (47, 91, 15, 10),
            (47, 200, 15, 10),
            (101, 229, 66, 10),
            (121, 1165, 3, 10),
            (94210, 94283, 24, 2),   # start_group reset
            (499, 4099, 16, 16)
        ]

        self.assertListEqual([], compare_ranges(tests))

    def test_separate_nodes_cases(self):
        """Seperate start/stop examples

        | start | stop  | TO | start | stop  | example        |
        |-------|-------|----|-------|-------|----------------|
        | True  | True  |    | True  | True  | (88, 2186, 15) |
        | True  | False |    | True  | True  | (88, 2100, 15) |
        | True  | False |    | True  | False | (88, 9990, 15) |
        | False | True  |    | True  | True  | (312, 9990, 15)|
        | False | True  |    | False | True  | (10, 2186, 15) |
        | False | False |    | False | False | (10, 9990, 15) |
        | False | False |    | True  | False | (312, 9990, 15)|
        | False | False |    | False | True  | (10, 15000, 15), (10, 150000, 15)|
        | False | False |    | True  | True  | (312, 15000, 15)|

        """


        test_all_cases = [(88, 2186, 15, 10),
                          (88, 2100, 15, 10),
                          (88, 9990, 15, 10),
                          (10, 2186, 15, 10),
                          (10, 9990, 15, 10),
                          (312, 9990, 15, 10),
                          (10, 15000, 15, 10),
                          (10, 150000, 15, 10),
                          (312, 15000, 15, 10)
                          ]

        self.assertListEqual([], compare_ranges(test_all_cases))


class GeneratedTestCases(unittest.TestCase):
    def param_generator(self, base = None):
        if not base:
            base = randint(2, 200)

        step = randint(1, 9999)
        start = randint(0, 1000000)
        stop = randint(start, 3000000)

        return start, stop, step, base

    def test_base_10(self):
        # warning takes a very long time now
        tests = [self.param_generator(10) for _ in range(1000000)]
        self.assertListEqual([], compare_ranges_par(tests))

    def test_base_16(self):
        tests = [self.param_generator(16) for _ in range(1000000)]
        self.assertListEqual([], compare_ranges_par(tests))

    def test_random_bases(self):
        tests = [self.param_generator() for _ in range(1000000)]
        self.assertListEqual([], compare_ranges_par(tests))


if __name__ == '__main__':
    unittest.main()
