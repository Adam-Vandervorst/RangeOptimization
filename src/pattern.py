from itertools import groupby
from math import lcm

from src.base_calc import numberToBase


def minimal_seq(xs: list[int]) -> list[int]:
    # `minimal_seq(xs)` returns the minimal sequence `r` such that `cycle(r) = cycle(xs)`
    # cycle([25, 24, 25, 24]) == cycle([25, 24])
    # cycle([4, 4, 4]) == cycle([4])
    # cycle([1, 2, 3]) == cycle([1, 2, 3])
    n = len(xs)
    pi = [0] * n
    for i in range(1, n):
        k = pi[i - 1]
        while k > 0 and xs[k] != xs[i]:
            k = pi[k - 1]
        if xs[k] == xs[i]:
            pi[i] = k + 1
        else:
            pi[i] = 0
    p = n - pi[-1]
    return xs[:p]


def pattern_ext(n, offset, base):
  # BASE10: pattern_(3) = [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
  # BASE10: pattern_(7) = [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
  # BASE10: pattern_(15) = [0, 15, 30, 45, 60, 75, 90, 5, 20, 35, 50, 65, 80, 95, 10, 25, 40, 55, 70, 85]
  # BASE10: pattern_(89) = [0, 89, 78, 67, 56, 45, 34, 23, 12, 1, 90, 79, 68, 57, 46, 35, 24, 13, 2, 91, 80, 69, 58, 47, 36, 25, 14, 3, 92, 81, 70, 59, 48, 37, 26, 15, 4, 93, 82, 71, 60, 49, 38, 27, 16, 5, 94, 83, 72, 61, 50, 39, 28, 17, 6, 95, 84, 73, 62, 51, 40, 29, 18, 7, 96, 85, 74, 63, 52, 41, 30, 19, 8, 97, 86, 75, 64, 53, 42, 31, 20, 9, 98, 87, 76, 65, 54, 43, 32, 21, 10, 99, 88, 77, 66, 55, 44, 33, 22, 11]
  assert offset >= 0
  assert offset < n

  order = len(numberToBase(n, base))
  return [(k + offset) % (base ** order) for k in range(0, lcm(base ** order, n), n)]


def repetition_offset(n, offset, base):
  assert offset >= 0
  assert offset < n
  # [1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1, 4, 7, 0, 3, 6, 9, 2, 5, 8, 1]
  # [0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9, 9, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 0]
  #  <  3  >  < 4      >  < 3   >  <  3  >  < 4      >  < 3   >  < 3   >  < 4      >  < 3   >  < 3   >
  # BASE10: repetition(3, 1) = [3, 4, 3]
  # [0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
  # [0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 7, 7, 8, 9, 9, 0, 1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 0, 1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 8, 9, 0, 0, 1, 2, 2, 3, 4]
  #  <2 >  1  <2 >  1  <2 >  1  1  <2 >  1  <2 >  1  <2 >  1  1  <2 >  1  <2 >  1  <2 >  1  1  <2 >  1  <2 >  1  <2 >  1  1  <2 >  1  <2 >  1  <2 >  1  1
  # BASE10: repetition(7, 0) = [2, 1, 2, 1, 2, 1, 1]
  # [2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2, 9, 6, 3, 0, 7, 4, 1, 8, 5, 2]
  # [0, 0, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 7, 7, 8, 9, 9, 0, 1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 0, 1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 8, 9, 0, 0, 1, 2, 2, 3, 4, 5, 5, 6, 7, 7, 8, 9, 9, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9, 9, 0, 1, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 8, 9, 0, 0, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 7, 7, 8, 9, 9, 0, 1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 0, 1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 8, 9, 0, 0, 1, 2, 2, 3, 4, 5, 5, 6, 7, 7, 8, 9, 9, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9, 9, 0, 1, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 8, 9, 0, 0, 1, 2, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 0, 0, 1, 2, 2, 3, 4, 4, 5, 6, 7, 7, 8, 9, 9, 0, 1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 8, 9, 0, 1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 8, 9, 0, 0, 1, 2, 2, 3, 4, 5, 5, 6, 7, 7, 8, 9, 9, 0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9, 9, 0, 1, 1, 2, 3, 3, 4, 5, 6, 6, 7, 8, 8, 9, 0]
  #  <2 >  1  1  <2 >  1  <2 >  1  <2 >  1  1  <2 >  1  <2 >  1  <2 >  1  1  <2 >  1  <2 >  1  <2 >  1  1  <2 >  1  <2 >  1  <2 >  1  1  <2 >  1  <2 >  1
  # BASE10: repetition(7, 0) = [2, 1, 1, 2, 1, 2, 1]
  return [sum(1 for _ in r) for k, r in groupby(map(lambda x: (x + offset)//base, range(0, base*n, n)))]


def repetition_ext(n, offset, base):
  order = len(numberToBase(n, base))
  return repetition_offset(n, offset, base**order)

