from pathlib import Path

p, rules = Path("14.txt").read_text().split("\n\n")
rules = dict(r.split(" -> ") for r in rules.split("\n") if r)
for _ in range(10):
    print(p)
    p = "".join(x + rules.get(x + y, "") for x, y in zip(p, p[1:])) + p[-1]
from collections import Counter

x = list(Counter(p).values())
print(max(x) - min(x))
