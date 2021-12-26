from __future__ import annotations
from icecream import ic
from pathlib import Path
from functools import cached_property, reduce
from dataclasses import dataclass, field
from typing import Iterable, List, Set, Tuple
from numpy.lib import math


@dataclass(frozen=True)
class Cube:
    left: Tuple
    right: Tuple

    @classmethod
    def make(cls, left: Tuple, right: Tuple) -> Cube:
        return Cube(tuple(left), tuple(right))

    @cached_property
    def area(self) -> int:
        return math.prod((max(0, b - a) for a, b in zip(self.left, self.right)))

    def __bool__(self) -> bool:
        return bool(self.area)

    def __contains__(self, cube: Cube) -> bool:
        return not any(
            cube.right[i] <= self.left[i] or cube.left[i] >= self.right[i]
            for i in range(3)
        )

    def __sub__(self, other: Cube) -> Cubes:
        return (
            [self]
            if other not in self
            else Cubes.make(
                *(
                    Cube(*map(tuple, x))
                    for x in (
                        (
                            [self.left[0], self.left[1], self.left[2]],
                            [other.left[0], self.right[1], self.right[2]],
                        ),
                        (
                            [other.right[0], self.left[1], self.left[2]],
                            [self.right[0], self.right[1], self.right[2]],
                        ),
                        (
                            [
                                max(x.left[0] for x in (self, other)),
                                self.left[1],
                                self.left[2],
                            ],
                            [
                                min(x.right[0] for x in (self, other)),
                                other.left[1],
                                self.right[2],
                            ],
                        ),
                        (
                            [
                                max(x.left[0] for x in (self, other)),
                                other.right[1],
                                self.left[2],
                            ],
                            [
                                min(x.right[0] for x in (self, other)),
                                self.right[1],
                                self.right[2],
                            ],
                        ),
                        (
                            [
                                max(x.left[0] for x in (self, other)),
                                max(x.left[1] for x in (self, other)),
                                self.left[2],
                            ],
                            [
                                min(x.right[0] for x in (self, other)),
                                min(x.right[1] for x in (self, other)),
                                other.left[2],
                            ],
                        ),
                        (
                            [
                                max(x.left[0] for x in (self, other)),
                                max(x.left[1] for x in (self, other)),
                                other.right[2],
                            ],
                            [
                                min(x.right[0] for x in (self, other)),
                                min(x.right[1] for x in (self, other)),
                                self.right[2],
                            ],
                        ),
                    )
                )
            )
        )


@dataclass(frozen=True)
class CubeOp:
    op: bool
    cube: Cube

    @classmethod
    def parse(self, s: str) -> CubeOp:
        toggle, cube = s.split(" ")
        toggle = toggle.strip() == "on"
        cube = tuple(
            tuple(map(int, (x.split("=")[-1] for x in c.split(".."))))
            for c in cube.split(",")
        )
        l, r = map(tuple, zip(*cube))
        return CubeOp(toggle, Cube.make(l, (rr + 1 for rr in r)))


@dataclass(frozen=True)
class Cubes:
    cubes: Set[Cube] = field(default_factory=set)

    @cached_property
    def area(self) -> int:
        return sum(c.area for c in self.cubes)

    @classmethod
    def make(cls, *cubes: List[Cube]) -> Cubes:
        return cls(set(filter(bool, cubes)))

    def __call__(self, op: CubeOp) -> Cubes:
        return (self + op.cube) if op.op else (self - op.cube)

    def __iter__(self) -> Iterable[Cube]:
        return iter(self.cubes)

    def __sub__(self, cube: Cube) -> Cubes:
        return Cubes.make(*(baby_cube for c in self.cubes for baby_cube in (c - cube)))

    def __add__(self, cube: Cube) -> Cubes:
        return Cubes.make(cube, *(self - cube).cubes)


ic(
    reduce(
        lambda x, y: x(y),
        map(
            CubeOp.parse,
            (
                line
                for line in Path("22.txt").read_text().splitlines(keepends=False)
                if not line.startswith("#")
            ),
        ),
        Cubes.make(),
    ).area
)
