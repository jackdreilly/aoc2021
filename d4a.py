import dataclasses
from typing import Iterable, List, Set
from functools import cached_property


@dataclasses.dataclass(frozen=True)
class Board:
    rows: List[List[int]]

    @cached_property
    def columns(self) -> List[List[int]]:
        return [list(row) for row in zip(*self.rows)]

    @cached_property
    def diags(self) -> List[List[int]]:
        return [
            [self.rows[i][i] for i in range(len(self.rows))],
            [self.rows[i][-i - 1] for i in range(len(self.rows))],
        ]

    @cached_property
    def members(self) -> Set[int]:
        return set(sum(self.rows, []))

    @property
    def seqs(self) -> Iterable[Set[int]]:
        for coll in (self.rows, self.columns):
            for row in coll:
                yield set(row)


@dataclasses.dataclass(frozen=True)
class Bingo:
    board: Board
    numbers: List[int]

    @cached_property
    def is_bingo(self) -> bool:
        for seq in self.board.seqs:
            if not seq - set(self.numbers):
                return True
        return False

    @cached_property
    def misses(self) -> Set[int]:
        return self.board.members - set(self.numbers)

    @cached_property
    def score(self) -> int:
        return sum(self.misses) * self.numbers[-1]


with open("i4a.txt", "r") as f:
    nums = list(map(int, f.readline().strip().split(",")))
    boards = [
        Board(
            [
                list(map(int, filter(len, x.strip().split(" "))))
                for x in y.strip().split("\n")
            ]
        )
        for y in f.read().strip().split("\n\n")
    ]


def solve(i=0):
    for bingo in (Bingo(board, nums[: i + 1]) for board in boards):
        if bingo.is_bingo:
            return bingo.score
    return solve(i + 1)


print(solve())
