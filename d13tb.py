import functools
from pathlib import Path

dots, moves = Path("13t.txt").read_text().split("\n\n")
dots = set(tuple(map(int, line.split(","))) for line in dots.split("\n"))
moves = [
    (dir, int(dist))
    for dir, dist in (
        line.split(" along ")[-1].split("=") for line in moves.split("\n") if line
    )
]


def reducer(dots, move):
    dir, dist = move
    return {
        (
            x if dir == "y" or x < dist else dist - (x - dist),
            y if dir == "x" or y < dist else dist - (y - dist),
        )
        for x, y in dots
    }


def gridify(dots):
    x = max(x for x, y in dots)
    y = max(y for x, y in dots)
    for j in range(y + 1):
        for i in range(x + 1):
            if (i, j) in dots:
                yield "x"
            else:
                yield " "
        yield "\n"


print(''.join(gridify(functools.reduce(reducer, moves, dots))))
