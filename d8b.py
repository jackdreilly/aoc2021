import functools
from pathlib import Path
from typing import Iterator, List
from dataclasses import dataclass
from functools import cached_property


@dataclass(frozen=True)
class Line:
    line: str

    def __iter__(self) -> Iterator[str]:
        return iter(self.words)

    @cached_property
    def words(self) -> List[str]:
        return [set(x) for chunk in self.line.split(" | ") for x in chunk.split(" ")]

    @cached_property
    def outputs(self) -> List[str]:
        return [
            set(x) for chunk in self.line.split(" | ")[-1:] for x in chunk.split(" ")
        ]


lines = [Line(line) for line in Path("i8.txt").read_text().split("\n") if line]


def solve_line(line: Line) -> int:
    one, seven, four = (
        next((word for word in line if len(word) == i), None) for i in (2, 3, 4)
    )
    A = seven - one
    C, F = one, one
    D = functools.reduce(lambda a, b: a & b, (word for word in line if len(word) == 5))
    G = D
    F = (
        functools.reduce(lambda a, b: a & b, (word for word in line if len(word) == 6))
        & F
    )
    C = C - F
    B = four - one - D
    D = four - one - B
    G = (
        functools.reduce(lambda a, b: a & b, (word for word in line if len(word) == 6))
        - four
        - A
    )
    E = set("abcdefg") - (A | B | C | D | F | G)
    translate = {k: next(iter(v)) for k, v in zip("abcdefg", [A, B, C, D, E, F, G])}
    words = {
        tuple(sorted(translate[x] for x in word)): str(i)
        for i, word in enumerate(
            (
                "abcefg",
                "cf",
                "acdeg",
                "acdfg",
                "bcdf",
                "abdfg",
                "abdefg",
                "acf",
                "abcdefg",
                "abcdfg",
            )
        )
    }
    return int("".join(words[tuple(sorted(word))] for word in line.outputs))


print(sum(map(solve_line, lines)))
