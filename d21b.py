from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import itertools


def memoize(f):
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = f(*args)
            # print(args[0], cache[args])
        return cache[args]

    return wrapper


@dataclass(frozen=True)
class Player:
    position: int
    score: int = 0

    def __add__(self, x: int) -> Player:
        position = (self.position + x) % 10
        return Player(position, self.score + (position or 10))


max_score = 21


@dataclass(frozen=True)
class Game:
    me: Player
    you: Player
    round: int = 0

    @classmethod
    def make(cls, i, j) -> Game:
        return Game(Player(i), Player(j))

    @property
    def win(self) -> bool:
        return self.me.score >= max_score

    @property
    def loss(self) -> bool:
        return self.you.score >= max_score

    @property
    def next(self) -> Iterable[Player]:
        for i in itertools.product(range(1, 4), repeat=3):
            yield self + sum(i)

    def __add__(self, x: int) -> Game:
        return Game(
            self.me if (self.round % 2) else (self.me + x),
            self.you if not (self.round % 2) else (self.you + x),
            self.round + 1,
        )


@memoize
def wins(game: Game) -> int:
    return 1 if game.win else 0 if game.loss else sum(map(wins, game.next))


print(wins(Game.make(2, 7)))
