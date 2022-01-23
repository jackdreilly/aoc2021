from __future__ import annotations
from collections import defaultdict

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from random import randint
from typing import Callable, ClassVar, Dict, List, Sequence, Tuple, Union
from black import sys

from devtools import debug
from icecream import ic
from pydantic import BaseModel


class OpType(Enum):
    inp = "inp"
    add = "add"
    mul = "mul"
    div = "div"
    mod = "mod"
    eql = "eql"


class Var(Enum):
    w = "w"
    x = "x"
    y = "y"
    z = "z"


class Op(BaseModel):
    op: OpType
    a: Var
    b: Union[Var, int] = None

    registry: ClassVar[Dict[OpType, Callable]] = {}

    class Config:
        frozen = True

    @property
    def string(self) -> str:
        return " ".join(
            str(x)
            for x in (self.op.value, self.a.value, getattr(self.b, "value", self.b))
            if x is not None
        )

    def apply(self, alu: ALU) -> Dict[Var, int]:
        return self.registry[self.op](self, alu)


def reg(op_type: OpType):
    def helper(fn):
        Op.registry[op_type] = fn
        return fn

    return helper


@reg(OpType.inp)
def inp(op: Op, alu: ALU):
    a, *rest = alu.inputs
    return {op.a: a, "inputs": rest}


@reg(OpType.add)
def add(op: Op, alu: ALU):
    return {op.a: alu.registers[op.a] + alu.get(op.b)}


@reg(OpType.mul)
def mul(op: Op, alu: ALU):
    return {op.a: alu.registers[op.a] * alu.get(op.b)}


@reg(OpType.div)
def div(op: Op, alu: ALU):
    return {op.a: alu.registers[op.a] // alu.get(op.b)}


@reg(OpType.mod)
def mod(op: Op, alu: ALU):
    return {op.a: alu.registers[op.a] % alu.get(op.b)}


@reg(OpType.eql)
def eql(op: Op, alu: ALU):
    return {op.a: int(alu.registers[op.a] == alu.get(op.b))}


@dataclass(frozen=True)
class ALU:
    inputs: List[int]
    ops: Sequence[Op] = tuple(
        Op.parse_obj(dict(zip(("op", "a", "b"), l.split(" "))))
        for l in Path(sys.argv[1]).read_text().splitlines()
    )
    registers: Dict[Var, int] = field(default_factory=lambda: defaultdict(int))

    @property
    def show(self):
        print(
            " ".join(
                [str(self.registers[v]) for v in Var]
                + [self.ops[0].string if self.ops else ""]
            )
        )

    def get(self, v: Union[Var, int]) -> int:
        return self.registers[v] if isinstance(v, Var) else v

    @property
    def eval(self) -> bool:
        self.show
        if not self.ops:
            return not self.registers[Var.z]
        op, *ops = self.ops
        try:
            result = op.apply(self)
            inputs = result.pop("inputs", self.inputs)
            return ALU(inputs, ops, defaultdict(int, {**self.registers, **result})).eval
        except ZeroDivisionError:
            return False

    @classmethod
    def make(cls, *inputs) -> ALU:
        return ALU(inputs=inputs)


import itertools
alu = ALU.make(*map(int, input()))
print(alu.eval)
# debug(
#     list(
#         (a, {bb[1] for bb in b})
#         for a, b in itertools.groupby(
#             sorted(enumerate(alu.ops), key=lambda x: (x[0] % 18, x[0])),
#             lambda x: x[0] % 18,
#         )
#     )
# )
