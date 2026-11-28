from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Literal:
    value: int | bool


@dataclass(frozen=True)
class Variable:
    name: str


@dataclass(frozen=True)
class Unary:
    operator: str
    operand: Any


@dataclass(frozen=True)
class Binary:
    left: Any
    operator: str
    right: Any


@dataclass(frozen=True)
class Assignment:
    name: str
    expression: Any


@dataclass(frozen=True)
class Print:
    expression: Any


@dataclass(frozen=True)
class Block:
    statements: list[Any]


@dataclass(frozen=True)
class If:
    condition: Any
    then_branch: Any
    else_branch: Any | None = None


@dataclass(frozen=True)
class While:
    condition: Any
    body: Any


@dataclass(frozen=True)
class For:
    initialization: Assignment
    condition: Any
    update: Assignment
    body: Any


@dataclass(frozen=True)
class Program:
    statements: list[Any]
