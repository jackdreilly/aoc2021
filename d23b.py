from __future__ import annotations
from collections import defaultdict
from itertools import islice
from icecream import ic

from typing import DefaultDict, Tuple

cfg = "bcbdadca"
cfg = "dcdbbaac"
# cfg = "bcbddcbadbacadca"
total_rows = len(cfg) // 4


positions = [(0, i) for i in range(11)] + [
    (i, j) for i in range(1, total_rows + 1) for j in range(2, 10, 2)
]
letter_home = {"A": 2, "B": 4, "C": 6, "D": 8}
letter_scores = {l: 10 ** i for i, l in enumerate("ABCD")}


def path_fn(a, b, c, d):
    for i in range(a - 1, 0, -1):
        yield i, b
    for i in islice(range(b, d, -1 if b > d else 1), 1 if not a else 0, None):
        yield 0, i
    for i in range(0, c + 1):
        yield i, d


def game_string(game):
    return "\n".join(
        "".join(
            game[(i, j)] or ("." if j in range(2, 10, 2) or not i else "#")
            for j in range(11)
        )
        for i in range(total_rows + 1)
    )


_cache = {}


class Min:
    score = float("inf")


def min_score(
    game: DefaultDict[Tuple[int, int], str], gen: int = 0, previous_score: int = 0
) -> int:
    s = game_string(game)
    if s in _cache:
        return _cache[s] + previous_score
    if previous_score > Min.score:
        return float("inf")
    score = previous_score

    def move(a, b, c, d, e):
        new_game = defaultdict(str, game)
        new_game.pop((a, b))
        new_game[(c, d)] = e
        return new_game, sum(1 for _ in path_fn(a, b, c, d)) * letter_scores[letter]

    tops = {
        letter: next(
            i
            for i in range(1, total_rows + 2)
            if all(
                (game[((j), letter_home[letter])] == (letter))
                for j in range((i), total_rows + 1)
            )
        )
        for letter in "ABCD"
        if (
            all(
                game[(i, letter_home[letter])] in (letter, "")
                for i in range(1, total_rows + 1)
            )
        )
    }
    while True:
        for (i, j), letter in list(game.items()):
            if not (letter):
                continue
            if (top := (tops.get(letter))) and (j) != (letter_home[letter]):
                if any(
                    (game[(i, j)])
                    for i, j in path_fn(i, j, top - 1, letter_home[letter])
                ):
                    continue
                game, other_score = move(i, j, top - 1, letter_home[letter], letter)
                score += other_score
                tops[letter] -= 1
                break
        else:
            break
    if all(
        game[(i, j)] == l
        for l, j in letter_home.items()
        for i in range(1, total_rows + 1)
    ):
        if score < Min.score:
            Min.score = score
            print(score)
        _cache[s] = score - previous_score
        return score

    min_score_ = float("inf")
    for (i, j), letter in list(game.items()):
        if not letter or not i:
            continue
        if ((j) == (letter_home[letter])) and i >= ((tops).get((letter), 100)):
            continue
        for k in range(11):
            if k == j:
                continue
            if any(game[l] for l in path_fn(i, j, 0, k)):
                continue
            new_game, other_score = move(i, j, 0, k, letter)
            min_score_ = min(
                min_score_,
                min_score(new_game, gen + 1, score + other_score),
            )
    _cache[s] = min_score_ - previous_score
    return min_score_


def init(cfg):
    return defaultdict(
        str, {(i // 4 + 1, (i % 4) * 2 + 2): l.upper() for i, l in enumerate(cfg)}
    )


print(min_score(init(cfg)))
