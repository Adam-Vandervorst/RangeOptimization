class Node:
    @classmethod
    def from_values(cls, vs, l):
        return cls(dict.fromkeys(vs, ()), l)

    @classmethod
    def restrict_node(cls, n: 'Node', ks: list[int], l):
        return cls({k: n.cd[k] for k in ks}, l)

    @classmethod
    def from_children(cls, ks, cs, l):
        ks = list(ks)
        cs = list(cs)
        assert len(ks) == len(cs)
        return cls(dict(zip(ks, cs)), l)

    def __init__(self, cd, l):
        self.idc = len(l)  # node id
        self.cd = cd  # dict of outgoing edges
        l.append(self)

    def used(self, s: set):
        for k, v in self.cd.items():
            if isinstance(v, Node):
                if v not in s:
                    v.used(s)
        s.add(self)

    def paths(self):
        for k, v in self.cd.items():
            if isinstance(v, Node):
                for p in v.paths():
                    yield [k] + p
            else:
                yield [k]

    def graphviz(self):
        for k, v in self.cd.items():
            if isinstance(v, Node):
                print(f"n{self.idc} -> n{v.idc} [label={k}]")
            else:
                print(f"n{self.idc} -> {k}")

    def graphviz_abstract(self, draw_vs=False):
        cs = {v for k, v in self.cd.items() if isinstance(v, Node)}
        for c in cs:
            print(f"n{self.idc} -> n{c.idc}")
        if draw_vs:
            vs = {k for k, v in self.cd.items() if not isinstance(v, Node)}
            if vs:
                print(f"n{self.idc} [label=\"{vs}\"]")
            else:
                print(f"n{self.idc} [label=\"{{}}\"]")

    def full_dict(self):
        def rec(n):
            return {k: rec(v) for k, v in n.cd.items()} if isinstance(n, Node) else str(n)

        return {k: rec(v) for k, v in self.cd.items()}

    def __repr__(self):
        nested = {k: str(v) for k, v in self.cd.items()}
        return f"N({self.idc}, {nested})"

    def __str__(self):
        return f"N{self.idc}"
