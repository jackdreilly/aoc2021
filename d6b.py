from pathlib import Path

cache = {}
print(
    sum(
        (
            num_fish := lambda day, remaining: cache.setdefault(
                (day, remaining),
                None
                if (day, remaining) in cache
                else 1
                if day <= remaining
                else num_fish(day - 1, remaining - 1)
                if remaining
                else (num_fish(day - 1, 6) + num_fish(day - 1, 8)),
            )
        )(256, int(x))
        for x in Path("i6a.txt").read_text().split(",")
    )
)
