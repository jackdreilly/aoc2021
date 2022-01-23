from __future__ import annotations

from collections import defaultdict
from itertools import islice
from typing import DefaultDict, Tuple
from icecream import ic

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


def memoize(fn):
    cache = {}

    def inner(x, *a, **b):
        args = game_string(x)
        if args not in cache:
            cache[args] = fn(x, *a, **b)
        return cache[args]

    return inner


def print_game(game):
    ...
    # print()
    # print(game)
    # print()
    # print(game_string(game))
    # print()
    # input()


@memoize
def min_score(game: DefaultDict[Tuple[int, int], str], history=[]) -> int:
    score = 0

    def move(a, b, c, d, e):
        new_game = defaultdict(str, game)
        new_game.pop((a, b))
        new_game[(c, d)] = e
        print_game(new_game)
        new_history = [*history, (c, d, e)]
        return (
            new_game,
            sum(1 for _ in path_fn(a, b, c, d)) * letter_scores[letter],
            new_history,
        )

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
    g,h = game, history
    class X:
        game = g
        history = h

    for (i, j), letter in list(X.game.items()):
        if not (letter):
            continue
        if (top := (tops.get(letter))) and (j) != (letter_home[letter]):
            if any(
                (X.game[(i, j)]) for i, j in path_fn(i, j, top - 1, letter_home[letter])
            ):
                continue
            X.game, other_score, X.history = move(
                i, j, top - 1, letter_home[letter], letter
            )
            score += other_score
            tops[letter] -= 1
    game = X.game
    history = X.history
    if all(
        game[(i, j)] == l
        for l, j in letter_home.items()
        for i in range(1, total_rows + 1)
    ):
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
            new_game, other_score, new_history = move(i, j, 0, k, letter)
            other_score += min_score(new_game, new_history)
            min_score_ = min(min_score_, other_score)
            if not history:
                ic(i, j, k, min_score_, new_history)
    return min_score_ + score


def init(cfg):
    return defaultdict(
        str, {(i // 4 + 1, (i % 4) * 2 + 2): l.upper() for i, l in enumerate(cfg)}
    )


# print(
#     min_score(
#         defaultdict(
#             str,
#             {
#                 (2, 2): "A",
#                 (2, 6): "C",
#                 (0, 0): "B",
#                 (0, 1): "C",
#                 (0, 2): "B",
#                 (0, 10): "A",
#                 (1, 8): "D",
#                 (2, 8): "D",
#             },
#         )
#     )
# )
print(min_score(init(cfg)))
