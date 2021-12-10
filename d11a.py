import functools
from pathlib import Path

flipped = {"{": "}", "[": "]", "(": ")", "<": ">"}
flipped2 = {v: k for k, v in flipped.items()}


def score(line: str, stack: list = None) -> int:
    if stack is None:
        stack = []
    if not line:
        return functools.reduce(lambda x, y: x * 5 + " )]}>".index(y), stack[::-1], 0)
    head, *tail = line
    if head in flipped:
        stack.append(flipped[head])
        return score(tail, stack)
    if not stack:
        return 0
    if head == stack[-1]:
        stack.pop()
        return score(tail, stack)
    return 0

scores = sorted(filter(bool, map(score, Path("11.txt").read_text().splitlines())))
print(scores[len(scores) // 2])
