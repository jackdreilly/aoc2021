from __future__ import annotations
from pathlib import Path
import functools
from typing import List
import numpy as np


grid = np.array(
    [[int(x) for x in y] for y in Path("12.txt").read_text().splitlines()]
)

flash_count = 0
for round in range(100):
    grid += np.ones(grid.shape, int)
    queue = []
    seen = set()
    while True:
        new_members = set(zip(*np.where(grid > 9))) - seen
        seen |= new_members
        queue.extend(new_members)
        if not queue:
            break
        x, y = queue.pop(0)
        grid[max(0, x - 1) : min(x + 2, 10), max(0, y - 1) : min(10, y + 2)] += 1
    for x, y in seen:
        grid[x, y] = 0
    flash_count += len(seen)
print(flash_count)
