from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from io import StringIO
from math import cos, pi, sin
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Tuple

import numpy as np
from numpy.lib.npyio import loadtxt


def _rotations():
    def x(i):
        return np.matrix(
            [1, 0, 0, 0, cos(i), -sin(i), 0, sin(i), cos(i)], dtype=int
        ).reshape(3, 3)

    def y(i):
        return np.matrix(
            [cos(i), 0, sin(i), 0, 1, 0, -sin(i), 0, cos(i)], dtype=int
        ).reshape(3, 3)

    def z(i):
        return np.matrix(
            [cos(i), -sin(i), 0, sin(i), cos(i), 0, 0, 0, 1], dtype=int
        ).reshape(3, 3)

    yield from (x(i * pi / 2) for i in range(4))
    yield from (z(2 * pi / 2) * x(i * pi / 2) for i in range(4))
    yield from (z(1 * pi / 2) * y(i * pi / 2) for i in range(4))
    yield from (z(3 * pi / 2) * y(i * pi / 2) for i in range(4))
    yield from (y(1 * pi / 2) * z(i * pi / 2) for i in range(4))
    yield from (y(3 * pi / 2) * z(i * pi / 2) for i in range(4))


rotations = list(_rotations())

scanners = [
    np.matrix(loadtxt(StringIO(x.strip().split("-\n")[-1]), delimiter=",", dtype=int))
    for x in Path("19.ex.txt").read_text().split("\n\n")
]


@dataclass(frozen=True)
class Projector:
    rotation: np.matrix
    pre_translation: np.matrix
    post_translation: np.matrix

    def __call__(self, x):
        return (self.rotation * (x - self.pre_translation).T).T + self.post_translation


@dataclass(frozen=True)
class Projectors:
    projectors: DefaultDict[int, Dict[int, Projector]] = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(bool))
    )

    def put(self, project_from, project_to, projector):
        self.projectors[project_from][project_to] = projector

    @property
    def keys(self) -> List[Tuple[int, int]]:
        return list((i, j) for i, p in self.projectors.items() for j in p)

    def path(self, project_from, project_to, history=[]):
        print("path", project_from, project_to, history)
        return (
            (project_from, project_to)
            if self.projectors[project_from][project_to]
            else min(
                (
                    (
                        project_from,
                        *path,
                    )
                    for path in (
                        self.path(other_to, project_to, [*history, project_from])
                        for other_to in self.projectors[project_from]
                        if other_to not in history and other_to != project_to
                    )
                    if path
                ),
                key=len,
                default=None,
            )
        )

    def _project(self, x, a, *rest):
        return x if not rest else self._project(self.projectors[a][rest[0]](x), *rest)

    def project(self, x, project_from, project_to):
        print("project", project_from, project_to)
        return (
            x
            if project_from == project_to
            else (
                (path := self.path(project_from, project_to))
                and self._project(x, *path)
            )
        )


projectors = Projectors()


for i_scanner_a, scanner_a in enumerate(scanners):
    for i_scanner_b, scanner_b in enumerate(scanners):
        if i_scanner_a == i_scanner_b or projectors.path(i_scanner_b, 0):
            continue
        print(i_scanner_a, i_scanner_b)
        done = False
        for i_reference_a, reference_a in enumerate(scanner_a):
            normalized_beacons_a = scanner_a - reference_a
            for i_reference_b, reference_b in enumerate(scanner_b):
                normalized_beacons_b = scanner_b - reference_b
                for ir, rotation in enumerate(rotations):
                    rotated_beacons_b = (rotation * normalized_beacons_b.T).T
                    if (
                        len(
                            set(map(tuple, list(np.array(normalized_beacons_a))))
                            & set(map(tuple, list(np.array(rotated_beacons_b))))
                        )
                        >= 12
                    ):
                        done = True
                        projectors.put(
                            i_scanner_b,
                            i_scanner_a,
                            Projector(rotation, reference_b, reference_a),
                        )
                        break
            if done:
                break
import pickle

with open("d19.ex.pickle", "wb") as f:
    pickle.dump({k: dict(v) for k, v in projectors.projectors.items()}, f)

print(
    len(
        {
            row
            for i, scanner in enumerate(scanners)
            for rows in projectors.project(scanner, i, 0)
            for row in map(tuple, rows.tolist())
        }
    )
)
