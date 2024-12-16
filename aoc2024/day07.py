from __future__ import annotations
import dataclasses
import itertools
import math
import operator
import typing
import aoc2024


@dataclasses.dataclass
class Equation:
    expected: int
    operands: tuple[int, ...]

    @classmethod
    def from_line(cls, line: str) -> Equation:
        answer_str, _, values_str = line.partition(":")
        return cls(
            expected=int(answer_str),
            operands=tuple(map(int, values_str.split())),
        )

    def iter_calculations(
        self, operators: tuple[typing.Callable, ...]
    ) -> typing.Iterator[int]:
        for ops in itertools.product(operators, repeat=len(self.operands) - 1):
            result = self.operands[0]
            for op, operand in zip(ops, self.operands[1:], strict=True):
                result = op(result, operand)
            yield result

    def has_match(self, operators: tuple[typing.Callable, ...]) -> bool:
        return any(
            result == self.expected
            for result in self.iter_calculations(operators=operators)
        )

    def __hash__(self) -> int:
        return hash((self.expected, self.operands))


def get_equations(path_to_input: str) -> list[Equation]:
    with open(file=path_to_input) as f:
        return list(map(Equation.from_line, f))


@aoc2024.expects(12553187650171)
def part_one(path_to_input: str) -> int:
    equations = get_equations(path_to_input=path_to_input)
    return sum(
        equation.expected
        for equation in equations
        if equation.has_match(operators=(operator.add, operator.mul))
    )


def concat(a: int, b: int) -> int:
    digits = int(math.log10(b) + 1)
    return (10**digits * a) + b


@aoc2024.skip_slow
@aoc2024.expects(96779702119491)
def part_two(path_to_input: str) -> int:
    equations = get_equations(path_to_input=path_to_input)
    return sum(
        equation.expected
        for equation in equations
        if equation.has_match(
            operators=(operator.add, operator.mul, concat),
        )
    )
