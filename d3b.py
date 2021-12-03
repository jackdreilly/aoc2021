from pathlib import Path
import math


def num(
    rule,
    i=0,
    lines=[list(map(int, x)) for x in Path("i3a.txt").read_text().splitlines()],
):
    return (
        int("".join(map(str, lines[0])), 2)
        if len(lines) == 1
        else num(
            rule,
            i + 1,
            list(
                filter(
                    lambda l: (l[i] == rule)
                    == bool(int(sum(ll[i] for ll in lines) * 2 / len(lines))),
                    lines,
                )
            ),
        )
    )


print(math.prod(map(num, range(2))))
