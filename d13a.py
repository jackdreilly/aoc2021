from pathlib import Path

edges = [
    tuple(x[::i])
    for x in [tuple(x.split("-")) for x in Path("13.txt").read_text().splitlines()]
    for i in (1, -1)
]
n = {k: {v for u, v in edges if u == k} for k, _ in edges}


def n_paths(history=None, special: str = None):
    if not history:
        for special in {k for k in n if k.lower() == k and k != "start" and k != "end"}:
            yield from n_paths(['start'], special)
        return
    if history[-1] == "end":
        yield tuple(history)
        return
    for v in n[history[-1]]:
        if v !=' start' and (
            v not in history
            or v.upper() == v
            or (
                v == special
                and sum(1 for x in history if x == special) == 1
            )
        ):
            yield from n_paths(history + [v], special)


print(len(set(n_paths())))
