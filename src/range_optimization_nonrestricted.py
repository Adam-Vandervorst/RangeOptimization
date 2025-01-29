# -*- coding: utf-8 -*-
"""Range optimization nonrestricted.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19iuMpPz9PdFVWMzWta6mt8HR_f8XybUu
"""

from itertools import groupby, repeat, cycle, accumulate, takewhile, islice
from math import gcd

from src.base_calc import numberToBase, order, to_number, to_size
from src.node import Node
from src.pattern import minimal_seq, pattern_ext, repetition_ext
from src.range_utility import find_last_number_of_range, strip_equal_start, number_of_nodes_per_layer, find_group



def nth(it, n):
    for i in range(n):
        x = next(it)
    return x


def crange(start: int, stop: int, step: int, base: int, debug = False) -> tuple[Node, list[Node]]:
  BASE = base
  assert base > 1
  assert step > 0
  assert start >= 0
  assert start <= stop

  if stop == start:
    return (Node({}, []), [])

  start_split_1 = numberToBase(start, base)

  if stop - start <= step:
    l = []
    prev_node = None
    if order(step, base) >= order(start, base):
      curr_node = Node({start: None}, l)
    else:
      trail, leaf = start_split_1[:-(order(step, base) + 1)], to_number(start_split_1[-(order(step, base) + 1):], base)
      trail.reverse()
      for s in [leaf] + trail:
        curr_node = Node({s: prev_node}, l)
        prev_node = curr_node

      # you can use this instead of the if/else for simplicity. BUT an inconsitency arrises with the other trees since other trees have number of order(step), in their leaf nodes, and with following code this special case returns leafs of order 0. So use the if/else above for consistency.
      # for s in reversed(start_split_1):
      #   curr_node = Node({s: prev_node}, l)
      #   prev_node = curr_node

    return curr_node, l


  last_number = find_last_number_of_range(start, stop, step)
  last_number_split = numberToBase(last_number, base)
  start_split = to_size(start_split_1, len(last_number_split))
  assert len(last_number_split) == len(start_split)
  offset = start%step

  std_nodes = int(step/gcd(BASE**(order(step, base) + 1), step))
  # print("std nodes", std_nodes)

  start_split_, last_number_split_, to_add = strip_equal_start(start_split, last_number_split)



  # print("last number", last_number)
  if debug: print(last_number_split)
  if debug: print(start, start_split)

  # print("to add", to_add)

  # calculate the number of nodes in each layer, which is not the lowest or highest layer
  size_intermediate_layers = number_of_nodes_per_layer(start_split_, last_number_split_, step, base)
  # print("size_intermediate_layers", size_intermediate_layers)





  pat = minimal_seq(pattern_ext(step, offset, base))

  # the next two are also calculated in the find_group method (not efficient?)
  pat_start_idx = pat.index(to_number(start_split_[-(order(step, base) + 1):], base))
  pat_stop_idx = pat.index(to_number(last_number_split[-(order(step, base) + 1):], base))

  if debug: print("pattern", pat)
  # print("first idx", pat_start_idx)
  # print("stop idx", pat_stop_idx)

  r1 = repetition_ext(step, offset, base)
    # compress r1 only if pattern is also compressed
  if len(pat) == sum(minimal_seq(r1)):
    r1_ = minimal_seq(r1)
  else:
    r1_ = r1

  assert pat_start_idx <= sum(r1_)

  # print("r1", r1)
  # print("r1_", r1_)


  start_group, start_idx = find_group(pat, r1_, to_number(start_split_[-(order(step, base) + 1):], base))
  separate_start_group = (start_idx != 0)

  stop_group, stop_idx = find_group(pat, r1_, to_number(last_number_split[-(order(step, base) + 1):], base))
  separate_stop_group = (stop_idx != (r1_[stop_group] - 1))

  if debug: print("(start group, start index)", (start_group, start_idx))
  # print("(stop group, stop index)", (stop_group, stop_idx))


  # print("separate start", separate_start_group)
  # print("separate stop", separate_stop_group)



  # bottom layer
  l = []
  lv1 = []

  pat_it = iter(cycle(pat))

  if len(last_number_split_) == (order(step, base) + 1):
    lv1_node = Node(dict(zip(pat[pat_start_idx:pat_stop_idx + 1], repeat(None))), l)
    lvs = [[lv1_node]]
    to_add.reverse()
    for e in to_add:
      lvs.append([Node({e: lvs[-1][0]}, l)])

    return lvs[-1][0], l

  for tk in r1_:
    lv1.append(Node(dict(zip(islice(pat_it, tk), repeat(None))), l))

  lvs = [lv1]

  # extra start node
  curr_start_node = None
  curr_start_idx = - (order(step, base) + 2)

  if separate_start_group:
    last_idx_start_group = pat_start_idx + r1_[start_group] - (start_idx + 1)
    # print("last_idx_start_group", last_idx_start_group)

    lv1_start_node = Node(dict(zip(pat[pat_start_idx:last_idx_start_group + 1], repeat(None))), l)
    # print("start lvl", lv1_start_node.cd)

    curr_start_node = lv1_start_node

  # extra stop node
  curr_stop_node = None

  if separate_stop_group:
    first_idx_stop_group = pat_stop_idx - stop_idx
    if debug: print("last_idx_stop_group", first_idx_stop_group)


    lv1_stop_node = Node(dict(zip(pat[first_idx_stop_group:pat_stop_idx + 1], repeat(None))), l)
    if debug: print("start lvl stop node", lv1_stop_node.cd)

    curr_stop_node = lv1_stop_node

  if order(last_number, base) == order(step, base) + 1:
    if debug: print("NEW CASE")

  # intermediate layers

  size_intermediate_layers.reverse()
  next_start_group = (start_group + 1)%len(r1_)

  std_nodes_ = len(r1_)
  eq_stop_node = stop_group

  for i, nns in enumerate(size_intermediate_layers):
    if debug: print("LAYER", i)

    if debug: print(separate_start_group, separate_stop_group)
    # print("stop group", stop_group)
    # print("stop_groups_to_skip", stop_groups_to_skip)

    lv_curr = []
    lv_prev = lvs[-1]
    # lv_stop = []


    # print("prev nodes", [l.idc for l in lv_prev])

    stop_groups_to_skip = (eq_stop_node - last_number_split_[curr_start_idx]) % std_nodes_

    if separate_start_group:  #checked
      lv_prev_it = iter(cycle(lv_prev))
      list(islice(lv_prev_it, next_start_group))
      v = [curr_start_node] + list(islice(lv_prev_it, BASE - start_split_[curr_start_idx] - 1))

      next_start_node = Node(dict(zip(range(start_split_[curr_start_idx], BASE), v)), l)
      # print("next start node", next_start_node, next_start_node.cd)

      curr_start_node = next_start_node




    if not separate_start_group:

      # print("start idx", curr_start_idx)
      # print("start number", start_split_[curr_start_idx])

      if start_split_[curr_start_idx] > 0:
        # print("CASE start_split[curr_start_idx] > 0")
        lv_prev_it = iter(cycle(lv_prev))
        list(islice(lv_prev_it, start_group))
        separate_start_group = True
        curr_start_node = Node(dict(zip(range(start_split_[curr_start_idx], BASE), islice(lv_prev_it, (BASE - start_split_[curr_start_idx])))), l)

        #  print("current start node", curr_start_node, curr_start_node.cd)


      else:
        if debug: print("CASE start_split[curr_start_idx] == 0")
        # print("curr_start", start_split_[curr_start_idx])
        if debug: print("I will skip", start_group)
        lv_prev_it = iter(cycle(lv_prev))
        list(islice(lv_prev_it, start_group))   # ???



    next_eq_stop_node = None
    first_node = list(islice(lv_prev_it, 1))
    peek_node = first_node

    for n in range(nns):
      d = dict(zip(range(BASE), peek_node + list(islice(lv_prev_it, BASE - 1))))
      if d[last_number_split_[curr_start_idx]] == lv_prev[eq_stop_node]:
        next_eq_stop_node = n
      lv_curr.append(Node(d, l))

      peek_node = list(islice(lv_prev_it, 1))
      if peek_node == first_node:
        break



    if next_eq_stop_node is None:
      # This should never occur
      raise NotImplementedError
      pass


    if separate_stop_group: #checked
      lv_prev_it_stop = iter(cycle(lv_prev))
      list(islice(lv_prev_it_stop, stop_groups_to_skip))

      # print("stop number", last_number_split_[curr_start_idx])
      v = list(islice(lv_prev_it_stop, last_number_split_[curr_start_idx])) + [curr_stop_node]

      next_stop_node = Node(dict(zip(range(0, last_number_split_[curr_start_idx] + 1), v)), l)
      # print("next stop node", next_stop_node, next_stop_node.cd)

      curr_stop_node = next_stop_node

    if not separate_stop_group:
      if last_number_split[curr_start_idx] < BASE - 1:    # checked (88, 2100, 15)
        # print("case last_number_split[curr_start_idx] < BASE - 1")
        lv_prev_it_stop = iter(cycle(lv_prev))

        list(islice(lv_prev_it_stop, stop_groups_to_skip))

        separate_stop_group = True
        curr_stop_node = Node(dict(zip(range(0, last_number_split_[curr_start_idx] + 1), islice(lv_prev_it_stop, last_number_split_[curr_start_idx] + 1))), l)
        # print("curr stop node", curr_stop_node, curr_stop_node.cd)


      else:
        # print("case last_number_split[curr_start_idx] == BASE - 1")   # test (88, 9990, 15)
        pass

    curr_start_idx -= 1
    lvs.append(lv_curr)
    next_start_group = 0
    std_nodes_ = std_nodes
    eq_stop_node = next_eq_stop_node
    start_group = 0


  if debug: print("end", separate_start_group, separate_stop_group)

  # top layer
  lv_top = []

  lv_prev_it = iter(cycle(lvs[-1]))

  if separate_start_group and not separate_stop_group:
    list(islice(lv_prev_it, next_start_group))
    d = [curr_start_node] + list(islice(lv_prev_it, BASE))

    list(islice(lv_prev_it, 1))
    # print("last nr", last_number_split_[0])

    lv_top.append(Node(dict(zip(range(start_split_[0], last_number_split_[0] + 1), d)), l))

  elif separate_start_group and separate_stop_group:   # checked
    list(islice(lv_prev_it, next_start_group))
    number_normal = last_number_split_[0] - start_split_[0] - 1

    # list(islice(lv_prev_it, 2))
    # print("number_normal", number_normal)

    d = [curr_start_node] + list(islice(lv_prev_it, number_normal)) + [curr_stop_node]
    lv_top.append(Node(dict(zip(range(start_split_[0], start_split_[0] + number_normal + 2), d)), l))

  elif not separate_start_group and separate_stop_group:
    list(islice(lv_prev_it, start_group))
    number_normal = last_number_split_[0] - start_split_[0]
    d = list(islice(lv_prev_it, number_normal)) + [curr_stop_node]
    lv_top.append(Node(dict(zip(range(start_split_[0], start_split_[0] + number_normal + 1), d)), l))


  elif not separate_start_group and not separate_stop_group:  # checked
    list(islice(lv_prev_it, start_group))
    lv_top.append(Node(dict(zip(range(start_split_[0], last_number_split_[0] + 1), islice(lv_prev_it, BASE))), l))

  lvs.append(lv_top)
  to_add.reverse()
  for e in to_add:
    lvs.append([Node({e: lvs[-1][0]}, l)])

  return lvs[-1][0], l



def to_number_special(p: list[int], o: int, base: int) -> int:
  # BASE = 10 => to_number_special([3, 2, 15], 1) = 3215
  # BASE = 10 => to_number_special([3, 2, 15], 2) = 32015
  return p[-1] + sum((base**(i + o + 1))*e for i, e in enumerate(reversed(p[:-1])))



def print_graph(l):
  print("digraph G { \n ranksep=3")
  for n in l: n.graphviz()
  print("}")



if __name__ == '__main__':
  base = 2
  # good edge cases (1002, 3), (2130, 3), (5201, 3)
  # good start cases: dangly edges: (3, 301, 199), (3, 4125, 4129), (3, 199, 321)
  # (827, 2977, 8)
  # (121, 1165, 3)
  # (841, 1275, 7)
  # start, stop, step = (37, 137, 20)  # BASE 16
  # start, stop, step = (94, 2000, 8)
  # start, stop, step = (100000, 292815, 80)
  start, stop, step = (94210, 94283, 24)
  start, stop, step = (94210, 94283, 24)


  rn, l = crange(start, stop, step, base)
  print("BASE", base)
  # print(repr(rn))

  # print(sorted(map(tuple, rn.paths())))
  r = [i for i in range(start, stop, step)]
  print("real  ", [to_number_special(i, order(step, base), base) for i in (sorted(map(tuple, rn.paths())))])
  print("wanted", r)
  # assert(r == [to_number_special(i, order(step, base), base) for i in (sorted(map(tuple, rn.paths())))])
  print(len(r))
  # print(max(map(to_number, rn.paths())))

  print("#wanted: ", len(range(start, stop, step)), "#real: ", sum(1 for _ in rn.paths()))
  print("check: ", len(range(start, stop, step)), "#real: ", sum(1 for _ in rn.paths()))

  ns = (map(lambda x: to_number_special(list(x), order(step, base), base), rn.paths()))
  m = start % step
  for n in ns:
    if not n % step == m:
      print("INCORRECT NUMBERS from", n)
      break
  print()
  print_graph(l)