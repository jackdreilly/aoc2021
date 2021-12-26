from pathlib import Path
from functools import reduce
import itertools
from icecream import ic


def parse(x):
    toggle, cube = x.split(" ")
    toggle = toggle.strip() == "on"
    cube = tuple(
        tuple(map(int, (x.split("=")[-1] for x in c.split(".."))))
        for c in cube.split(",")
    )
    return toggle, cube


print(
    len(
        reduce(
            lambda x, y: x | y[1] if y[0] else x - y[1],
            (
                (
                    toggle,
                    {
                        *itertools.product(
                            *(range(max(-50, a), min(50, b) + 1) for a, b in cube)
                        )
                    },
                )
                for toggle, cube in map(
                    parse, Path("22.txt").read_text().splitlines(keepends=False)
                )
            ),
            set(),
        )
    )
)
