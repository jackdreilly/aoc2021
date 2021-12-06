from pathlib import Path

cache = {}


def num_fish(day, remaining) -> int:
    return cache.setdefault(
        (day, remaining),
        None
        if (day, remaining) in cache
        else 1
        if day <= remaining
        else num_fish(day - 1, remaining - 1)
        if remaining
        else (num_fish(day - 1, 6) + num_fish(day - 1, 8)),
    )


print(sum(num_fish(80, int(x)) for x in Path("i6a.txt").read_text().split(",")))
