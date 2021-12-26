from __future__ import annotations
from dataclasses import dataclass, field
from functools import cached_property, reduce
from itertools import product
from pathlib import Path
from typing import Iterable, Set, Tuple
from icecream import ic


@dataclass(frozen=True)
class Grid:
    values: Set[Tuple[int, int]] = field(default_factory=set)
    round: int = 0

    @cached_property
    def min_x(self) -> int:
        return min(i for i, j in self.values)

    @cached_property
    def max_x(self) -> int:
        return max(i for i, j in self.values)

    @cached_property
    def min_y(self) -> int:
        return min(j for i, j in self.values)

    @cached_property
    def max_y(self) -> int:
        return max(j for i, j in self.values)

    @property
    def search_iterator(self) -> Iterable[Tuple[int, int]]:
        return {
            (i + si, j + sj)
            for i in range(self.min_x - 4, self.max_x + 4)
            for j in range(self.min_y - 4, self.max_y + 4)
            for si, sj in product(range(-2, 3), repeat=2)
        }

    def value(self, i: int, j: int) -> bool:
        return (i, j) in self.values or (
            self.round % 2
            and 0 in decoder
            and (i < self.min_x or i > self.max_x or j < self.min_y or j > self.max_y)
        )

    def bin(self, i: int, j: int):
        return int(
            "".join(
                map(
                    str,
                    map(
                        int,
                        (
                            self.value(i + a, j + b)
                            for a, b in product(range(-1, 2), repeat=2)
                        ),
                    ),
                )
            ),
            2,
        )

    def transform(self, i: int, j: int) -> bool:
        return self.bin(i, j) in decoder

    def __str__(self) -> str:
        return "\n".join(
            "".join(
                "#" if (i, j) in self.values else "."
                for j in range(
                    min(j for i, j in self.values), max(j for i, j in self.values) + 1
                )
            )
            for i in range(
                min(i for i, j in self.values), max(i for i, j in self.values) + 1
            )
        )

    @property
    def count(self) -> int:
        return len(self.values)

    @property
    def enhance(self) -> Grid:
        return Grid(
            {(i, j) for i, j in self.search_iterator if self.transform(i, j)},
            self.round + 1,
        )


a, b = Path("20.txt").read_text().split("\n\n")
decoder = {i for i, aa in enumerate(a.strip()) if aa == "#"}
b = Grid(
    {
        (i, j)
        for i, x in enumerate(b.strip().splitlines(False))
        for j, y in enumerate(x)
        if y == "#"
    }
)
print(len(reduce(lambda a,b: a.enhance, range(50), b).values))
