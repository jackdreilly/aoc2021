from __future__ import annotations
import heapq
from pathlib import Path
from typing import Generic, List, TypeVar
from dataclasses import dataclass


T = TypeVar("T")


@dataclass(frozen=True)
class HeapNode(Generic[T]):
    value: T
    priority: int

    def __lt__(self, other):
        return self.priority < other.priority


@dataclass(frozen=True)
class Heap(Generic[T]):
    heap: List[HeapNode[T]]

    def __bool__(self):
        return bool(self.heap)

    @classmethod
    def make(cls, *values: List[T]):
        v = [HeapNode(v, 0) for v in values]
        heapq.heapify(v)
        return cls(v)

    def pop(self) -> T:
        return heapq.heappop(self.heap).value

    def add(self, value: T, priority: int):
        heapq.heappush(self.heap, HeapNode(value, priority))
        return self


grid = [
    [int(x) for x in y] for y in map(str, Path("15.txt").read_text().splitlines())
]
grid = [
    [(col + a + b - 1) % 9 + 1 for b in range(5) for col in row]
    for a in range(5)
    for row in grid
]


n, m = len(grid), len(grid[0])


distances = [
    [0 if i == n - 1 and j == m - 1 else float("inf") for j in range(m)]
    for i in range(n)
]

heap = Heap.make((n - 1, m - 1))
visited = set()
while heap:
    (i, j) = heap.pop()
    if (i, j) in visited:
        continue
    visited.add((i, j))
    for (di, dj) in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if 0 <= i + di < n and 0 <= j + dj < m:
            distances[i + di][j + dj] = min(
                distances[i + di][j + dj], distances[i][j] + grid[i][j]
            )
            if not (i + di) and not (j + dj):
                print(distances[0][0])
                exit()
            heap.add((i + di, j + dj), distances[i + di][j + dj])
