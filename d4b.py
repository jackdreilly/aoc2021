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

    @cached_property
    def seqs(self) -> Iterable[Set[int]]:
        return [set(seq) for coll in (self.rows, self.columns) for seq in coll]


@dataclasses.dataclass(frozen=True)
class Bingo:
    board: Board
    numbers: List[int]

    @property
    def last_number(self) -> int:
        return self.numbers[-1]

    @cached_property
    def numset(self) -> Set[int]:
        return set(self.numbers)

    @cached_property
    def is_bingo(self) -> bool:
        return any(not seq - self.numset for seq in self.board.seqs)

    @cached_property
    def misses(self) -> Set[int]:
        return self.board.members - self.numset

    @cached_property
    def score(self) -> int:
        return sum(self.misses) * self.last_number


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
    if any(not Bingo(board, nums[: i + 1]).is_bingo for board in boards):
        return solve(i + 1)
    return Bingo(
        next(board for board in boards if not Bingo(board, nums[:i]).is_bingo),
        nums[: i + 1],
    ).score


print(solve())