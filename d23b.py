from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from queue import PriorityQueue
from random import randint
from typing import Dict, List


@dataclass(frozen=True, order=True)
class Grid:
    score: int
    data: List[List[str]] = field(compare=False)

    @classmethod
    def parse(cls, d: str) -> Grid:
        d = d.replace("\n", "").strip()
        return cls(0, [d[i * 11 : (i + 1) * 11] for i in range(N_ROWS + 1)])

    @property
    def completed(self) -> bool:
        return (
            str(self).strip()
            == """
...........
..A.B.C.D..
..A.B.C.D..
..A.B.C.D..
..A.B.C.D..
""".strip()
        )

    def __setitem__(self, key, value):
        self.data[key[0]][key[1]] = value

    def __getitem__(self, key):
        return self.data[key[0]][key[1]]

    def __str__(self):
        return "\n".join("".join(row) for row in self.data)

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, __o: object) -> bool:
        return str(self) == str(__o)

    def copy(self, score: int) -> Grid:
        return Grid(score, list(map(list, self.data)))

    def empty(self, row, col) -> bool:
        return self[row, col] == "."

    @cached_property
    def finish_rows(self) -> Dict[str, int]:
        d = {}
        for letter, col in (("A", 2), ("B", 4), ("C", 6), ("D", 8)):
            finish = None
            for row in range(N_ROWS, 0, -1):
                if not finish:
                    if self.empty(row, col):
                        finish = row
                        continue
                    if self[row, col] != letter:
                        finish = None
                        break
                else:
                    if not self.empty(row, col):
                        finish = None
                        break
            d[letter] = finish
        return d

    def done(self, row, col) -> bool:
        if self.empty(row, col):
            return False
        l = self[row, col]
        if col != 2 * (ord(l) - ord("A")) + 2:
            return False
        finish = self.finish_rows[l]
        if not finish:
            return False
        return row > finish

    @property
    def next_states(self) -> List[Grid]:
        for rr, row_value in enumerate(self.data):
            for cc, col_value in enumerate(row_value):
                row = rr
                col = cc
                start_row = row
                start_col = col
                if col_value == ".":
                    continue
                if self.done(start_row, start_col):
                    continue
                letter_diff = ord(col_value) - ord("A")
                per_move = 10 ** (letter_diff + 1)
                home_col = 2 + 2 * letter_diff
                if not row:
                    finish = self.finish_rows[col_value]
                    if not finish:
                        continue
                    dir = 2 * int(start_col < home_col) - 1
                    dead = False
                    while col != home_col:
                        col += dir
                        if not self.empty(row, col):
                            dead = True
                            break
                    if dead:
                        continue
                    yield self.move(start_row, start_col, finish, home_col)
                    continue
                dead = False
                while row:
                    row -= 1
                    if not self.empty(row, start_col):
                        dead = True
                        break
                if dead:
                    continue
                for final_col in (0, 1, 3, 5, 7, 9, 10):
                    dead = False
                    col = start_col
                    dir = 2 * (start_col < final_col) - 1
                    while col != final_col:
                        col += dir
                        if not self.empty(row, col):
                            dead = True
                            break
                    if dead:
                        continue
                    yield self.move(start_row, start_col, 0, final_col)

    def move(self, start_row, start_col, finish, home_col) -> Grid:
        v = self[start_row, start_col]
        letter_diff = ord(v) - ord("A")
        per_move = 10 ** (letter_diff)
        score = (
            self.score
            + (abs(start_col - home_col) + abs(start_row - finish)) * per_move
        )
        new_grid = self.copy(score)
        new_grid[start_row, start_col] = "."
        new_grid[finish, home_col] = v
        return new_grid


data = "DCDBDCBADBACBAAC"
# data = "DCDBBAAC"
# data = "BCBDDCBADBACADCA"
N_ROWS = len(data) // 4
data = [data[i * 4 : (i + 1) * 4] for i in range(N_ROWS)]
blank = Grid(0, [["."] * 11 for _ in range(1 + N_ROWS)])
for i, row in enumerate(data):
    for j, col in enumerate(row):
        blank[i + 1, j * 2 + 2] = col

seen = set()
todo: PriorityQueue[Grid] = PriorityQueue()
todo.put(blank)
while not todo.empty():
    state = todo.get()
    if not randint(0, 1000):
        print(state.score)
    # if state.score == 14303:
    #     showwww = True
    #     print("#" * 80)
    #     print(str(state))
    #     print("#" * 80)
    #     print()
    # if state.score > 14303:
    #     exit()

    if state.completed:
        print(state.score)
        exit()
    if state in seen:
        continue
    seen.add(state)
    for tp in state.next_states:
        todo.put(tp)


# @dataclass(frozen=True)
# class State:
#     letter: int
#     row: int
#     column: int
#     move: int = 0


# states = [
#     (State(letter=1, row=1, column=8, move=0), 0, 3),
#     (State(letter=2, row=2, column=8, move=0), 0, 5),
#     (State(letter=3, row=1, column=6, move=0), 0, 7),
#     (State(letter=3, row=0, column=7, move=1), 2, 8),
#     (State(letter=0, row=2, column=6, move=0), 0, 10),
#     (State(letter=2, row=0, column=5, move=1), 2, 6),
#     (State(letter=2, row=1, column=4, move=0), 0, 5),
#     (State(letter=2, row=0, column=5, move=1), 1, 6),
#     (State(letter=0, row=2, column=4, move=0), 0, 9),
#     (State(letter=1, row=0, column=3, move=1), 2, 4),
#     (State(letter=3, row=1, column=2, move=0), 0, 3),
#     (State(letter=3, row=0, column=3, move=1), 1, 8),
#     (State(letter=1, row=2, column=2, move=0), 0, 3),
#     (State(letter=1, row=0, column=3, move=1), 1, 4),
#     (State(letter=0, row=0, column=9, move=1), 2, 2),
#     (State(letter=0, row=0, column=10, move=1), 1, 2),
# ]

# grid = blank
# for state, row, col in states:
#     grid = grid.move(state.row, state.column, row, col)
#     print(grid.score)
#     print(str(grid))
#     print()
# grid = Grid.parse(
#     """.........AA
# ......C.D..
# ..B.B.C.D.."""
# )
# print(str(grid))
# for ns in grid.next_states:
#     print(ns.score)
#     print(str(ns))
#     print()
