from math import gcd

from src.base_calc import to_digits, digit
from src.node import Node


def find_last_number_of_range(start: int, stop: int, step: int) -> int:
    rem = stop % step
    offset = start % step
    return stop + offset - rem - (step if offset >= rem else 0)


def find_group_and_index(pat: list[int], group_division: list[int], n: int) -> tuple[int, int, int]:
    idx = pat.index(n)

    p = 0
    for g_number, g_size in enumerate(group_division):
        g_place = idx - p
        p += g_size
        if p > idx:
            return idx, g_number, g_place


def strip_equal_start(l1: list[digit], l2: list[digit]) -> tuple[list[digit], list[digit], list[digit]]:
    assert len(l1) > 0 and len(l2) > 0
    start = []

    for i in range(len(l1)):
        if l1[i] == l2[i]:
            start.append(l1[i])
        else:
            break

    return l1[i:], l2[i:], start


def number_of_nodes_per_layer(start: list[digit], last_n: list[digit], step: int, base: int) -> list[int]:
    assert (len(start) == len(last_n))

    upper_layer_edges = last_n[0] - start[0] + 1  # number of edges starting from top node

    num_nodes = int(step / gcd(base ** (len(to_digits(step, base))), step))  # ??
    upper_layer_nodes = min(upper_layer_edges, num_nodes)

    num_intermediate_layers = (len(last_n) - 1) - len(to_digits(step, base))
    if num_intermediate_layers <= 0:
        return []
    size_intermediate_layers = [upper_layer_nodes]  # number of nodes in each layer

    prev_layer_nodes = upper_layer_nodes
    for l in range(num_intermediate_layers - 1):
        curr_layer_edges = prev_layer_nodes * base
        curr_layer_nodes = min(curr_layer_edges, num_nodes)
        size_intermediate_layers.append(curr_layer_nodes)
        prev_layer_nodes = curr_layer_nodes

    return size_intermediate_layers


def add_root(rn: 'Node', to_add: list[digit], alloc: 'list[Node]') -> Node:
    curr_node = rn
    for e in reversed(to_add):
        curr_node = Node.from_children([e], [curr_node], alloc)
    return curr_node

