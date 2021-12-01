from pathlib import Path

data = list(map(int, Path("d1a.txt").read_text().splitlines()))
print(
    sum(sum(data[i : i + 3]) < sum(data[i + 1 : i + 4]) for i in range(len(data) - 3))
)
