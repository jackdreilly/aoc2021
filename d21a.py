from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Tuple
from icecream import ic


@dataclass(frozen=True)
class Die:
    value: int = 1
    rolls: int = 0

    @property
    def next(self) -> Tuple[int, Die]:
        return sum(self.value + i for i in range(3)), Die(
            (self.value + 3) % 10, self.rolls + 3
        )


@dataclass(frozen=True)
class Player:
    position: int
    score: int = 0

    def roll(self, die: Die) -> Tuple[Player, Die]:
        roll, die = die.next
        position = (self.position + roll) % 10
        score = self.score + (position or 10)
        return Player(position, score), die


@dataclass(frozen=True)
class Game:
    active: Player
    next: Player
    die: Die = field(default_factory=Die)

    @classmethod
    def make(cls, a: int, b: int) -> Game:
        return Game(Player(a), Player(b))

    @property
    def players(self) -> Iterable[Player]:
        yield self.active
        yield self.next

    @property
    def play(self) -> int:
        return self.score or Game(self.next, *self.active.roll(self.die)).play

    @property
    def score(self) -> int:
        return self.is_over and self.die.rolls * min(p.score for p in self.players)

    @property
    def is_over(self) -> bool:
        return max(p.score for p in self.players) >= 1000


print(Game.make(2, 7).play)
