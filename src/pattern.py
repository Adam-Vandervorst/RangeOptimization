from itertools import groupby, cycle, islice, takewhile
from math import lcm

from src.base_calc import numberToBase


def minimal_seq(xs: list[int]) -> list[int]:
    # `minimal_seq(xs)` returns the minimal sequence `r` such that `cycle(r) = cycle(xs)`
    n = len(xs)
    if n == 0:
        return xs
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


def pattern_and_repetition(n, offset, base, extended=False):
    if extended:
        order = len(numberToBase(n, base))
        base = base**order
    if n == 0:
        return [offset]

    assert offset >= 0
    assert n < base
    assert offset < n
    assert offset < base

    # instead of using lcm, one can use as stop criterion that the first generated number is reached again
    # following code is also correct and tested
    res = [offset]
    rep = []
    c = 1
    k = offset + n
    while True:
        if k >= base:
            k -= base
            rep.append(c)
            c = 0
        if k == offset:
            break
        res.append(k)
        k += n
        c += 1
    # return [(k + offset) % base for k in range(0, lcm(base, n), n)]
    assert len(res) == lcm(base, n)/n
    assert len(set(res)) == len(res)  # TODO remove when not debugging
    return res, rep


def pattern(n, offset, base):
    if n == 0:
        return [offset]

    assert offset >= 0
    # assert offset < n
    assert n < base
    # assert offset < base

    # instead of using lcm, one can use as stop criterion that the first generated number is reached again
    # following code is also correct and tested
    res = [(k + offset) % base for k in range(0, lcm(base, n), n)]
    assert len(res) == lcm(base, n)/n
    assert len(set(res)) == len(res)  # TODO remove when not debugging
    return res

def pattern_ext(n, offset, base):
  if n == 0:
      return [offset]

  assert offset >= 0
  # assert offset < n     # if offset >= n, we can get a pattern (e.g. pattern_ext(3, 3, 10) = [3, 6, 9, 2, 5, 8, 1, 4, 7, 0]) such that the first and last element of the pattern belong to the same group

  order = len(numberToBase(n, base))
  return pattern(n, offset, base ** order)


def repetition_offset(n, offset, base):
  if n == 0:
    return [0]  # the answer here should be infinity! Since 0 is in no other case the answer, we use 0

  assert offset >= 0
  # assert offset < n  # if offset >= n, we can get a pattern (e.g. pattern_ext(3, 3, 10) = [3, 6, 9, 2, 5, 8, 1, 4, 7, 0]) such that the first and last element of the pattern belong to the same group

  # return pattern_and_repetition(n, offset, base)[1]
  return [sum(1 for _ in r) for k, r in groupby(map(lambda x: x//base, range(offset, offset + lcm(base, n), n)))]

def repetition_ext(n, offset, base):
  order = len(numberToBase(n, base))
  return repetition_offset(n, offset, base**order)

def one_up(rep3, base, num_up = 1):
    it = iter(cycle(rep3))

    if rep3 == [0]:
        return pattern_ext(num_up, 0, base)

    seq = []
    i = 0
    for n in islice(it, base ** 2):
        for n_ in range(n):
            seq.append(i)
            i = (i + num_up) % base
        i = (i + 1) % base

    return seq

