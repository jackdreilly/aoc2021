from __future__ import annotations
import random
from devtools import debug
import pickle
from dataclasses import dataclass
from typing import Counter, Dict, Iterable, List, Set, Tuple
from functools import cached_property
from icecream import ic


@dataclass(frozen=True)
class State:
    letter: int
    row: int
    column: int
    move: int = 0

    def next(self, row: int, column: int) -> State:
        return State(row=row, column=column, letter=self.letter, move=self.move + 1)

    def score(self, row: int, column: int) -> int:
        return (10 ** self.letter) * (abs(self.column - column) + abs(self.row - row))

    @cached_property
    def sort_tuple(self) -> Tuple[int, int, int]:
        return (self.letter, self.row, self.column)

    @cached_property
    def done(self) -> bool:
        return self.move == 2 or (self.is_home and self.column == 2)

    @cached_property
    def home_col(self) -> bool:
        return self.letter * 2 + 2

    @cached_property
    def is_home(self) -> bool:
        return self.home_col == self.column

    def path(self, row: int, col: int) -> Iterable[Tuple[int, int]]:
        if self.move:
            for col in (
                range(self.column + 1, col + 1)
                if self.column < col
                else range(self.column - 1, col - 1, -1)
            ):
                yield (self.row, col)
            for row in range(row + 1):
                yield (row, col)
            return
        for row in range(self.row - 1, row, -1):
            yield (row, self.column)
        for col in (
            range(self.column, col + 1)
            if self.column < col
            else range(self.column, col - 1, -1)
        ):
            yield (0, col)


_cache = {}


@dataclass(frozen=True)
class Game:
    states: Set[State]

    def letter_done(self, letter: int) -> bool:
        return all(s.done for s in self.states if s.letter == letter)

    def state_done(self, state: State) -> bool:
        return state.done or self.letter_done(state.letter)

    @cached_property
    def over(self) -> bool:
        return (sorted(x.sort_tuple for x in self.states)) == (
            sorted((l, 2 - c, l * 2 + 2) for l in range(4) for c in range(2))
        )

    def move(self, state: State, row: int, col: int) -> Game:
        return Game((self.states - {state}) | {state.next(row, col)})

    @cached_property
    def hash(self) -> int:
        return hash(tuple(sorted(x.sort_tuple for x in self.states)))

    @cached_property
    def min_score(self) -> Tuple[int, List[State]]:
        if random.random() < 0.001:
            print(len(_cache))
        if score := _cache.get(self.hash):
            return score
        if self.over:
            return 0, []
        else:

            def f(args):
                state, row, col = args
                score, history = self.move(state, row, col).min_score
                score += state.score(row, col)
                return score, [args, *history]

            score, history = min(
                map(f, self.moves),
                key=lambda x: x[0],
                default=(float("inf"), []),
            )
        _cache[self.hash] = (score, history)
        return score, history

    def letter(self, row: int, column: int):
        if state := self.occupied_squares.get((row, column)):
            return "ABCD"[state.letter]
        return "." if not row or column in range(2, 10, 2) else " "

    def __str__(self) -> str:
        return "\n\n".join(
            (
                (
                    "\n"
                    + "\n".join(
                        "".join(self.letter(row, col) for col in range(11))
                        for row in range(3)
                    )
                    + "\n"
                ),
                "",
            )
        )

    def __repr__(self) -> str:
        return str(self)

    @property
    def moves(self) -> Iterable[Tuple[State, int, int]]:
        return (
            (state, row, col)
            for state in self.states
            for row, col in self.state_moves(state)
        )

    @cached_property
    def occupied_squares(self) -> Dict[Tuple[int, int], State]:
        return {(s.row, s.column): s for s in self.states}

    def occupied(self, row: int, column: int) -> bool:
        return (row, column) in self.occupied_squares

    def legal(self, state: State, row: int, col: int) -> bool:
        return all(
            not self.occupied(row, col) for (row, col) in set(state.path(row, col))
        )

    def rows(self, state: State) -> Iterable[int]:
        yield 0 if not state.move else 2 if not self.occupied(2, state.home_col) else 1

    def cols(self, state: State) -> Iterable[int]:
        if state.move:
            yield state.home_col
            return
        yield from range(state.column)
        yield from range(state.column + 1, 11)

    def state_moves(self, state: State) -> Iterable[Tuple[int, int]]:
        return (
            []
            if self.state_done(state)
            else (
                (row, col)
                for row in self.rows(state)
                for col in self.cols(state)
                if self.legal(state, row, col)
            )
        )

    @classmethod
    def make(cls, cfg: str) -> Game:
        return cls(
            {
                State(
                    letter="ABCD".index(letter), row=i // 4 + 1, column=(i % 4) * 2 + 2
                )
                for i, letter in enumerate(cfg)
            }
        )


# for state, row, col in (
#     (State(1, 1, 6), 0, 3),
#     (State(2, 1, 4), 0, 5),
#     (State(2, 0, 5, 1), 1, 6),
#     (State(3, 2, 4), 0, 5),
#     (State(1, 0, 3, 1), 2, 4),
#     (State(1, 1, 2), 0, 3),
#     (State(1, 0, 3, 1), 1, 4),
#     (State(3, 1, 8), 0, 7),
#     (State(0, 2, 8), 0, 9),
#     (State(3, 0, 7, 1), 2, 8),
#     (State(3, 0, 5, 1), 1, 8),
#     (State(0, 0, 9, 1), 1, 2),
#     # (State(1, 1, 6), 0, 3),
# ):
#     score += state.score(row, col)
#     game = game.move(state, row, col)
#     print(game)
# print(score)
# score, history = game.min_score

# with open("data.pkl", "wb") as f:
#     pickle.dump(history, f)
print(Game.make("DCDBBAAC").min_score)
# print(game)
# with open("data.pkl", "rb") as f:
#     history = pickle.load(f)
# from devtools import debug

# # print(score)
# score = 0
# for state, row, col in history[:4]:
#     debug(state)
#     debug((row, col))
#     score += state.score(row, col)
#     game = game.move(state, row, col)
#     print(game)
#     debug(game)
#     print(score)
# state = State(letter=1, row=1, column=2)
# assert state in game.states
# assert game.legal(state, 0, 1)
# game = game.move(state, 0, 1)
# assert state not in game.states
# debug(list(State(letter=0, row=2, column=2).path(0, 0)))
# assert not game.legal(State(letter=0, row=2, column=2), 0, 0)
# 20
# 40
# 200
# 200
# 2000
# 3000
# 30
# 40
# 3
# 3000
# 4000
# 8

# debug(
#     list(
#         Game(
#             states={
#                 State(
#                     letter=0,
#                     row=2,
#                     column=2,
#                     move=0,
#                 ),
#                 State(
#                     letter=3,
#                     row=2,
#                     column=4,
#                     move=0,
#                 ),
#                 State(
#                     letter=1,
#                     row=1,
#                     column=2,
#                     move=0,
#                 ),
#                 State(
#                     letter=3,
#                     row=2,
#                     column=8,
#                     move=2,
#                 ),
#                 State(
#                     letter=2,
#                     row=2,
#                     column=6,
#                     move=0,
#                 ),
#                 State(
#                     letter=2,
#                     row=1,
#                     column=4,
#                     move=0,
#                 ),
#                 State(
#                     letter=1,
#                     row=1,
#                     column=6,
#                     move=0,
#                 ),
#                 State(
#                     letter=0,
#                     row=0,
#                     column=4,
#                     move=1,
#                 ),
#             },
#         ).state_moves(State(letter=0, row=0, column=4, move=1))
#     )
# )
