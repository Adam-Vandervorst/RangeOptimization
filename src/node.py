from typing import Iterable


class Node:
    @classmethod
    def from_values(cls, ks: 'Iterable[int]', alloc: 'list[Node]'):
        d = dict.fromkeys(ks, None)
        assert len(d) > 0
        return cls(d, alloc)

    @classmethod
    def restrict_node(cls, n: 'Node', ks: 'Iterable[int]', alloc: 'list[Node]'):
        d = {k: n.cd[k] for k in ks}
        assert len(d) > 0
        return cls(d, alloc)

    @classmethod
    def from_children(cls, ks: 'Iterable[int]', cs: 'Iterable[Node]', alloc: 'list[Node]'):
        ks = list(ks)
        cs = list(cs)
        assert len(ks) == len(cs)
        assert len(ks) > 0
        return cls(dict(zip(ks, cs)), alloc)

    def __init__(self, cd: 'dict[int, Node | None]', alloc: 'list[Node]'):
        self.idc = len(alloc)  # node id
        self.cd = cd  # dict of outgoing edges
        alloc.append(self)

    def used(self, seen: 'set[Node]'):
        for k, v in self.cd.items():
            if v is not None and v not in seen:
                v.used(seen)
        seen.add(self)

    def paths(self):
        for k, v in self.cd.items():
            if v is None:
                yield [k]
            else:
                for p in v.paths():
                    yield [k] + p


    def graphviz(self):
        for k, v in self.cd.items():
            if v is None:
                print(f"n{self.idc} -> {k}")
            else:
                print(f"n{self.idc} -> n{v.idc} [label={k}]")

    def graphviz_abstract(self, draw_vs=False):
        cs = {v for k, v in self.cd.items() if v is not None}
        for c in cs:
            print(f"n{self.idc} -> n{c.idc}")
        if draw_vs:
            vs = {k for k, v in self.cd.items() if v is None}
            if vs:
                print(f"n{self.idc} [label=\"{vs}\"]")
            else:
                print(f"n{self.idc} [label=\"{{}}\"]")

    def full_dict(self):
        def rec(n):
            return {k: rec(v) for k, v in n.cd.items()} if n is not None else str(n)

        return {k: rec(v) for k, v in self.cd.items()}

    def __repr__(self):
        nested = {k: str(v) for k, v in self.cd.items()}
        return f"N({self.idc}, {nested})"

    def __str__(self):
        return f"N{self.idc}"
