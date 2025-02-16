from math import lcm
from time import monotonic
from collections import deque
from itertools import cycle, islice

from src.base_calc import to_digits, to_number, to_size
from src.leaf_extension import make_leaf_nodes, next_step, last_layer, last_layer_grouped
from src.node import Node
from src.pattern import pattern_and_repetition, pattern
from src.range_utility import (find_last_number_of_range, strip_equal_start, number_of_nodes_per_layer,
                               find_group_and_index, add_root)


def skip_elements(iterator, count):
    deque(islice(iterator, count), maxlen=0)


def base_layer_with_offset(offset, step, base, l, n_steps=None, grouped=False):
    step_digits = to_digits(step, base)
    n_layers = len(step_digits)

    assert n_layers > 1

    offset_digits = to_size(to_digits(offset, base), n_layers)

    lv_prev = make_leaf_nodes(offset_digits[-1], step_digits[-1], base, l, n_steps)

    for i in range(2, n_layers):
        lv_prev = next_step(offset_digits[-i:], step_digits[-i:], lv_prev, base, l, n_steps)

    if grouped:
        return last_layer_grouped(offset_digits, step_digits, lv_prev, base, l, n_steps)
    else:
        return last_layer(offset_digits, step_digits, lv_prev, base, l, n_steps)


def crange(start: int, stop: int, step: int, base: int, l: list[Node] = None) -> Node:
    assert base > 1
    assert step > 0
    assert start >= 0
    assert start < stop

    if l is None:
        l = []

    start_digits = to_digits(start, base)

    # Generate a tree with only the start number
    if stop - start <= step:
        n = Node.from_values([start_digits[-1]], l)
        return add_root(n, start_digits[:-1], l)

    last_number = find_last_number_of_range(start, stop, step)
    last_number_digits = to_digits(last_number, base)

    # mend size to be same for start and last number
    start_digits = to_size(start_digits, len(last_number_digits))

    # expected number of nodes per layer int(step / gcd(base ** step_order, step))

    truncated_start_digits, truncated_last_number_digits, to_add = strip_equal_start(start_digits, last_number_digits)

    return add_root(crange_core(step, base, truncated_start_digits, truncated_last_number_digits, l), to_add, l)


def crange_core(step: int, base: int, start_digits: list[int], stop_digits: list[int], l: list[Node] = None) -> Node:
    start = to_number(start_digits, base)
    stop = to_number(stop_digits, base)
    assert (stop - start) % step == 0
    step_order = len(to_digits(step, base))
    offset = start % step
    n_paths = ((stop - start) // step) + 1
    small_range = n_paths < (lcm(base**len(to_digits(step, base)), step)/step)
    if len(stop_digits) == step_order:
        # bottom layer (leaf nodes)
        # in the case there will only be one layer (only leaf nodes)
        # e.g. in base range(0, 9, 3) range(0, 45, 10), range(3500, 9000, 1500)
        if step < base:
            p = pattern(step, to_number(start_digits[-step_order:], base), base, n_paths)
            return Node.from_values(p, l)
        if small_range:
            return base_layer_with_offset(start, step, base, l, n_paths, grouped=True)[0]
        else:
            return base_layer_with_offset(offset, step, base, l, None, grouped=True)[0]

    pat, r1 = pattern_and_repetition(step, offset, base, extended=True)

    pat_start_idx, start_group, start_idx = find_group_and_index(pat, r1, to_number(start_digits[-step_order:], base))
    separate_start_group: bool = (start_idx != 0)
    assert pat_start_idx <= sum(r1)

    pat_stop_idx, stop_group, stop_idx = find_group_and_index(pat, r1, to_number(stop_digits[-step_order:], base))
    separate_stop_group: bool = (stop_idx != (r1[stop_group] - 1))

    assert (stop - start) % step == 0

    # make leaf layer
    if step < base:
        pat_it = iter(cycle(pat))
        lv1 = [Node.from_values(islice(pat_it, tk), l) for tk in r1]
    else:
        if small_range:  # also correct if always false; unused node optimization
            # print("start idx", pat_start_idx, pat_stop_idx)
            lv1 = base_layer_with_offset(start, step, base, l, n_paths)
            separate_start_group = False
            separate_stop_group = False

            start_group = 0
            stop_group = len(lv1) - 1
        else:
            lv1 = base_layer_with_offset(offset, step, base, l)

    lv_prev = lv1

    # extra start node
    curr_start_node = None
    curr_idx = - (step_order + 1)

    if separate_start_group:
        last_idx_start_group = pat_start_idx + r1[start_group] - (start_idx + 1)
        node_to_copy = lv1[start_group]  # this node contains the subtrees we want to share

        # for to_digits(p, base)[0] note the following
        # order(p) == step_order in this sub pattern, because p's with smaller order are always the first element of a group, and the first element of a group cannot be part of a seperate start group
        # for p in pat[pat_start_idx:last_idx_start_group + 1]: assert len(to_digits(p, base)) == step_order
        part_of_pat = [p//(base**(step_order-1)) for p in
                       pat[pat_start_idx:last_idx_start_group + 1]]

        curr_start_node = Node.restrict_node(node_to_copy, part_of_pat, l)

    # extra stop node
    curr_stop_node = None

    if separate_stop_group:
        first_idx_stop_group = pat_stop_idx - stop_idx
        node_to_copy = lv1[stop_group]
        # alternatively to_digits(p, base)[0] if len(to_digits(p, base)) == step_order else 0
        part_of_pat = [p//(base**(step_order-1)) for p in
                       pat[first_idx_stop_group:pat_stop_idx + 1]]

        curr_stop_node = Node.restrict_node(node_to_copy, part_of_pat, l)

    # intermediate layers
    # calculate the number of nodes in each layer, which is not the lowest or highest layer
    size_intermediate_layers = number_of_nodes_per_layer(start_digits, stop_digits, step, base)
    # correct both with or without the modulo (without modulo, we might go through one cycle more of the previous level nodes)
    next_start_group = (start_group + 1) % len(r1)

    to_skip = next_start_group if separate_start_group else start_group

    std_nodes = len(r1)
    eq_stop_node: int = stop_group

    for i, nns in enumerate(reversed(size_intermediate_layers)):
        lv_curr = []
        lv_prev_it = iter(cycle(lv_prev))

        skip_elements(lv_prev_it, to_skip)

        stop_groups_to_skip: int = (eq_stop_node - stop_digits[curr_idx]) % std_nodes
        if separate_start_group:
            nodes = [curr_start_node, *islice(lv_prev_it, base - start_digits[curr_idx] - 1)]
            curr_start_node = Node.from_children(range(start_digits[curr_idx], base), nodes, l)

        if not separate_start_group and start_digits[curr_idx] > 0:
            separate_start_group = True
            nodes = islice(lv_prev_it, base - start_digits[curr_idx])
            curr_start_node = Node.from_children(range(start_digits[curr_idx], base), nodes, l)

        next_eq_stop_node = None
        first_node = next(lv_prev_it)
        peek_node = first_node

        for n in range(nns):
            child_nodes = [peek_node, *islice(lv_prev_it, base - 1)]
            # The node that connects to the previous equivalent stop node with an edge labeled with the current stop-digit, is the new equivalent stop node
            if child_nodes[stop_digits[curr_idx]] == lv_prev[eq_stop_node]:
                next_eq_stop_node = n
            lv_curr.append(Node.from_children(range(base), child_nodes, l))

            peek_node = next(lv_prev_it)
            if peek_node == first_node:
                break

        if next_eq_stop_node is None and not small_range:
            raise RuntimeError("Unexpected condition: next_eq_stop_node should not be None.")

        lv_prev_it_stop = iter(cycle(lv_prev))
        skip_elements(lv_prev_it_stop, stop_groups_to_skip)

        if separate_stop_group:
            nodes = [*islice(lv_prev_it_stop, stop_digits[curr_idx]), curr_stop_node]
            curr_stop_node = Node.from_children(range(0, stop_digits[curr_idx] + 1), nodes, l)

        if not separate_stop_group and stop_digits[curr_idx] < base - 1:
            separate_stop_group = True
            nodes = islice(lv_prev_it_stop, stop_digits[curr_idx] + 1)
            curr_stop_node = Node.from_children(range(0, stop_digits[curr_idx] + 1), nodes, l)

        lv_prev = lv_curr

        curr_idx -= 1
        to_skip = 0
        eq_stop_node = next_eq_stop_node

    # top layer
    lv_prev_it = iter(cycle(lv_prev))
    skip_elements(lv_prev_it, to_skip)

    # number of middle nodes, +1 because inclusive
    slice_size = (stop_digits[0] - start_digits[0] + 1) - separate_start_group - separate_stop_group

    nodes = []
    if separate_start_group:
        nodes.append(curr_start_node)
    nodes.extend(islice(lv_prev_it, slice_size))
    if separate_stop_group:
        nodes.append(curr_stop_node)

    edge_labels = range(start_digits[0], stop_digits[0] + 1)
    top_node = Node.from_children(edge_labels, nodes, l)

    return top_node


def print_graph(l):
    print("digraph G { \n ranksep=3")
    for n in l: n.graphviz()
    print("}")


def abstract_graph(l, draw_vs=False):
    print("strict digraph G { \n ranksep=3")
    for n in l: n.graphviz_abstract(draw_vs)
    print("}")


def main(start, stop, step, base):
    l = []
    rn = crange(start, stop, step, base, l)
    print("BASE", base)
    # print(repr(rn))

    # print(sorted(map(tuple, rn.paths())))
    r = [i for i in range(start, stop, step)]
    print("real  ", [to_number(i, base) for i in (sorted(map(tuple, rn.paths())))])
    print("wanted", r)
    # assert(r == [to_number_special(i, order(step, base), base) for i in (sorted(map(tuple, rn.paths())))])
    print(len(r))
    # print(max(map(to_number, rn.paths())))

    print("#wanted: ", len(range(start, stop, step)), "#real: ", sum(1 for _ in rn.paths()))
    print("check: ", len(range(start, stop, step)), "#real: ", sum(1 for _ in rn.paths()))

    ns = (map(lambda x: to_number(list(x), base), rn.paths()))
    m = start % step
    for n in ns:
        if not n % step == m:
            print("INCORRECT NUMBERS from", n)
            break
    print()
    print_graph(l)

    print()
    print()
    print()

    # l_ = []
    # base_layer(125, 10, l_)
    # print_graph(l_)


def large_main(start, stop, step, base):
    from contextlib import redirect_stdout
    t0 = monotonic()
    l = []
    rn = crange(start, stop, step, base, l)
    s: set[Node] = set()
    rn.used(s)
    print("generating took:", monotonic() - t0)
    print("generated nodes:", len(l))
    print("useful nodes:", len(s))
    with open(f"r_{start}_{stop}_{step}_{base}.graphviz", 'w') as f:
        with redirect_stdout(f):
            abstract_graph(s, False)


if __name__ == '__main__':
    # main(0, 10000, 113, 10)
    large_main(6**8, 6**8 + 2*6**32 + 1, 6**32, 10)
    # large_main(0, 1000, 113, 10)
    # main(679668, 732633, 75429, 765)
    # main(923, 931, 93, 10)
