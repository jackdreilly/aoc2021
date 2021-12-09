from pathlib import Path
from math import prod

lookup = {
    (row, col): int(x)
    for row, line in enumerate(Path("i10.txt").read_text().splitlines())
    for col, x in enumerate(line)
}


def search(row, col, visited=None):
    visited = visited or set()
    visited.add((row, col))
    return 1 + sum(
        search(row + r, col + c, visited)
        for r, c in [[0, 1], [1, 0], [0, -1], [-1, 0]]
        if lookup.get((row + r, col + c), 10) < 9 and (row + r, col + c) not in visited
    )


print(
    prod(
        sorted(
            search(row, col)
            for (row, col), x in lookup.items()
            if all(
                x < lookup.get((row + r, col + c), 10)
                for r, c in [[0, 1], [1, 0], [0, -1], [-1, 0]]
            )
        )[-3:]
    )
)
