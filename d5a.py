from __future__ import annotations
from collections import defaultdict

from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Counter, Dict, List


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def parse(cls, s: str) -> Point:
        x, y = s.split(",")
        return cls(int(x), int(y))

    def __lt__(self, other: Point) -> bool:
        return (self.x, self.y) < (other.x, other.y)


class Direction(Enum):
    horizontal = 0
    vertical = 1
    diagonal = 2


@dataclass(frozen=True)
class Line:
    a: Point
    b: Point

    @cached_property
    def direction(self) -> Direction:
        return (
            Direction.vertical
            if self.a.x == self.b.x
            else Direction.horizontal
            if self.a.y == self.b.y
            else Direction.diagonal
        )

    @classmethod
    def parse(cls, line: str) -> Line:
        if not line.strip():
            return None
        a, b = line.strip().split(" -> ")
        return cls(*sorted((Point.parse(a), Point.parse(b))))

    @cached_property
    def all_points(self) -> List[Point]:
        if self.direction == Direction.vertical:
            return [Point(self.a.x, y) for y in range(self.a.y, self.b.y + 1)]
        if self.direction == Direction.horizontal:
            return [Point(x, self.a.y) for x in range(self.a.x, self.b.x + 1)]
        return []


@dataclass(frozen=True)
class Grid:
    lines: List[Line]

    @cached_property
    def occupancy(self) -> Dict[Point, int]:
        return defaultdict(
            lambda: 0, Counter(p for line in self.lines for p in line.all_points)
        )

    @cached_property
    def grid_view(self) -> str:
        return "\n".join(
            "".join(
                str(self.occupancy[Point(col, row)] or " ")
                for col in range(self.num_cols)
            )
            for row in range(self.num_rows)
        )

    @cached_property
    def num_rows(self) -> int:
        return max(p.y for p in self.occupancy) + 1

    @cached_property
    def num_cols(self) -> int:
        return max(p.x for p in self.occupancy) + 1

    @cached_property
    def intersections(self) -> List[Point]:
        return [p for p, c in self.occupancy.items() if c > 1]

    @classmethod
    def parse(cls, filename: str) -> Grid:
        return cls(list(map(Line.parse, Path(filename).read_text().splitlines())))


grid = Grid.parse("i5.txt")
print(len(grid.intersections))
# print(grid.grid_view)
