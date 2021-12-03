from pathlib import Path

lines = [list(map(int, x)) for x in Path("i3a.txt").read_text().splitlines()]
n = len(lines)
a = int("".join(str(int(sum(x) * 2 / n)) for x in zip(*lines)), 2)
b = ~a & ((1 << len(lines[0])) - 1)
print(a * b)
