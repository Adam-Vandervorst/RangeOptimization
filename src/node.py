

class Node:
    def __init__(self, cd, l):
        self.idc = len(l) # node id
        self.cd = cd      # dict of outgoing edges
        l.append(self)

    def paths(self):
        for k, v in self.cd.items():
            if v is None:
                yield [k]
            else:
                for p in v.paths():
                    yield [k] + p

    def numbers(self, base, offset, depth: int = 0):
        for k, v in self.cd.items():
            if v is None:
                yield k
            else:
                prefix = k * base**(offset - depth)
                for p in v.numbers(base, offset, depth + 1):
                    yield prefix + p

    def graphviz(self):
        for k, v in self.cd.items():
            if v is None:
                print(f"n{self.idc} -> {k}")
            else:
                print(f"n{self.idc} -> n{v.idc} [label={k}]")

    def __repr__(self):
        nested = {k: str(v) for k, v in self.cd.items()}
        return f"N({self.idc}, {nested})"

    def __str__(self):
        return f"N{self.idc}"