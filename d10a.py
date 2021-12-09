from pathlib import Path

lookup = {
    (row, col): int(x)
    for row, line in enumerate(Path("i10.txt").read_text().splitlines())
    for col, x in enumerate(line)
}

print(
    sum(
        x + 1
        for (row, col), x in lookup.items()
        if all(
            x < lookup.get((row + r, col + c), 10)
            for r, c in [[0, 1], [1, 0], [0, -1], [-1, 0]]
        )
    )
)
