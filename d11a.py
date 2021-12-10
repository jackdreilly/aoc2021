import functools
from pathlib import Path
from deepnone import dn

flipped = {"{": "}", "[": "]", "(": ")", "<": ">"}


def score(line: str, stack: list = []) -> int:
    if not line:
        return functools.reduce(lambda x, y: x * 5 + " )]}>".index(y), stack[::-1], 0)
    head, *tail = line
    return (
        score(tail, [*stack, flipped[head]])
        if head in flipped
        else score(tail, stack[:-1])
        if dn(stack)[-1] == head
        else 0
    )


scores = sorted(filter(bool, map(score, Path("11.txt").read_text().splitlines())))
print(scores[len(scores) // 2])