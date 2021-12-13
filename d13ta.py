from pathlib import Path

dots, moves = Path("13t.txt").read_text().split("\n\n")
dots = [tuple(map(int, line.split(","))) for line in dots.split("\n")]
moves = [
    (dir, int(dist))
    for dir, dist in (
        line.split(" along ")[-1].split("=") for line in moves.split("\n") if line
    )
]
dir, dist = moves[0]
print(
    len(
        {
            (
                x if dir == "y" or x < dist else dist - (x - dist),
                y if dir == "x" or y < dist else dist - (y - dist),
            )
            for x, y in dots
        }
    )
)
