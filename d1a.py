from pathlib import Path

data = list(map(int, Path("d1a.txt").read_text().splitlines()))
print(sum(b > a for a, b in zip(data, data[1:])))
