from pathlib import Path
from collections import defaultdict, Counter

p, rules = Path("14.txt").read_text().split("\n\n")
rules = dict(r.split(" -> ") for r in rules.split("\n") if r)
counts = defaultdict(int, Counter(x + y for x, y in zip(p, p[1:])))

for _ in range(40):
    new_counts = defaultdict(int)
    for k, v in list(counts.items()):
        x = rules.get(k)
        if x:
            new_counts[k[0] + x] += v
            new_counts[x + k[1]] += v
        else:
            new_counts[k] += v
    counts = new_counts
outcount = defaultdict(int)
for (a, b), v in counts.items():
    outcount[a] += v
outcount[p[-1]] += 1
print(max(outcount.values()) - min(outcount.values()))
