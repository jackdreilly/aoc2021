from __future__ import annotations

from typer import style
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Iterable, List, Optional, Union
from deepnone import dn


@dataclass(unsafe_hash=True)
class Tree:
    l: Union[Tree, int] = None
    r: Union[Tree, int] = None
    parent: Optional[Tree] = None
    _dfs_cache: List[Tree] = None

    @cached_property
    def root(self) -> Tree:
        return dn(self).parent.root.or_first

    @property
    def _dfs(self) -> Iterable[Tree]:
        yield from dn(self.l)._dfs
        yield self
        yield from dn(self.r)._dfs

    @property
    def dfs(self) -> Iterable[Tree]:
        return self.root._dfs_cache

    @property
    def is_leaf(self) -> bool:
        return any(isinstance(x, int) for x in (self.l, self.r))

    @property
    def left_neighbor(self) -> Optional[True]:
        return next(
            (
                x
                for x in list(self.dfs)[
                    : next(i for i, x in enumerate(self.dfs) if self is x)
                ][::-1]
                if x.is_leaf
            ),
            None,
        )

    @property
    def right_neighbor(self) -> Optional[True]:
        return next(
            (
                x
                for x in list(self.dfs)[
                    next(i for i, x in enumerate(self.dfs) if self is x) + 1 :
                ]
                if x.is_leaf
            ),
            None,
        )

    @property
    def reduce(self) -> Tree:
        self._dfs_cache = list(self._dfs)
        return self.reduce if self.find else self

    def __str__(self):
        return "".join(map(self.style, map(str, ("[", self.l, ",", self.r, "]"))))

    def style(self, s: str) -> str:
        return style(s, "red" if s.isnumeric() and int(s) > 9 else self.color)

    @property
    def color(self) -> str:
        return ["cyan", "green", "blue", "yellow", "magenta"][self.depth - 1]

    def __repr__(self) -> str:
        return str(self)

    @property
    def find(self) -> bool:
        return self.explode or self.split

    @property
    def explode(self) -> bool:
        for tree in self.dfs:
            if tree.depth < 5:
                continue
            if n := tree.left_neighbor:
                if isinstance(n.r, int):
                    n.r += tree.l
                else:
                    n.l += tree.l
            if n := tree.right_neighbor:
                if isinstance(n.l, int):
                    n.l += tree.r
                else:
                    n.r += tree.r
            if tree.parent.l == tree:
                tree.parent.l = 0
            else:
                tree.parent.r = 0
            return True

    @property
    def split(self) -> bool:
        for tree in self.dfs:
            for k in "lr":
                value = getattr(tree, k)
                if isinstance(value, int) and value > 9:
                    setattr(
                        tree,
                        k,
                        Tree.make(
                            (
                                value // 2,
                                (value + 1) // 2,
                            ),
                            tree,
                        ),
                    )
                    return True

    @property
    def depth(self) -> int:
        return 1 + dn(self.parent).depth.default(0)

    def __add__(self, other: Tree) -> Tree:
        me = Tree()
        self.parent = me
        other.parent = me
        me.l = self
        me.r = other
        return me

    @classmethod
    def make(cls, list_values: List, parent: Tree = None) -> Tree:
        if isinstance(list_values, int):
            return list_values
        if isinstance(list_values, str):
            list_values = eval(list_values)
        me = Tree(parent=parent)
        l, r = (cls.make(x, me) for x in list_values)
        me.l = l
        me.r = r
        return me

    @property
    def magnitude(self) -> int:
        return self.reduce._magnitude

    @property
    def _magnitude(self) -> int:
        return dn(self.l)._magnitude.or_first * 3 + dn(self.r)._magnitude.or_first * 2


trees = [
    x
    for x in Path("18.ex.txt").read_text().replace("+ ", "").strip().split("\n")
    if not x.startswith("#")
]


print(
    max(
        (Tree.make(x) + Tree.make(y)).magnitude
        for i, x in enumerate(trees)
        for j, y in enumerate(trees)
        if i != j
    )
)
