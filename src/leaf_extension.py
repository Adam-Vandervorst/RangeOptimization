from collections import deque
from itertools import cycle, islice, takewhile, accumulate
from math import lcm

from src.base_calc import to_number, to_size, to_digits
from src.node import Node
from src.pattern import pattern, repetition_offset, pattern_and_repetition


def make_leaf_nodes(start, step, base, l, n_steps=None):
    assert start < base
    assert step < base

    pat = pattern(step, start, base, n_steps)

    return [Node.from_values([p], l) for p in pat]


def next_step(start_split, step_split, prev_nodes, base, l, n_steps=None):
    prev_step = to_number(step_split[1:], base)

    if prev_step == 0:
        pat = pattern(step_split[0], start_split[0], base, n_steps)
    else:
        pat = pattern(to_number(step_split, base), to_number(start_split, base), base ** len(step_split), n_steps, cutoff=base**(len(step_split) - 1))
    lv_prev_it = iter(cycle(prev_nodes))
    return [Node.from_children([p], [next(lv_prev_it)], l) for p in pat]


def last_layer(start_split, step_split, prev_nodes, base, l, n_steps=None):
    pat = pattern(to_number(step_split, base), to_number(start_split, base), base ** len(step_split), n_steps, base**(len(step_split) - 1))
    r = repetition_offset(to_number(step_split, base), to_number(start_split, base), base ** len(step_split))
    if n_steps:
        assert len(pat) == n_steps
        num_groups, total = deque(takewhile(lambda x: x[1] <= n_steps, enumerate(accumulate(r))), maxlen=1).pop()
        r = r[:num_groups+1]
        assert len(pat) >= len(r)
        if n_steps != total:
            r.append(n_steps - total)
        # assert (len(pat) == sum(r))  # slow test

    pat_it = iter(cycle(pat))
    lv_prev_it = iter(cycle(prev_nodes))
    return [Node.from_children(islice(pat_it, tk), islice(lv_prev_it, tk), l) for tk in r]


def last_layer_grouped(start_split, step_split, prev_nodes, base, l, n_steps=None):
    pat = pattern(to_number(step_split, base), to_number(start_split, base), base ** len(step_split), n_steps, cutoff=base**(len(step_split) - 1))

    lv_prev_it = iter(cycle(prev_nodes))
    return [Node.from_children(pat, islice(lv_prev_it, len(pat)), l)]
