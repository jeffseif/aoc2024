"""
--- Day 7: Bridge Repair ---
The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge, though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.
The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?

Your puzzle answer was 12553187650171.

--- Part Two ---
The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
192: 17 8 14 can be made true using 17 || 8 + 14.
Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?

Your puzzle answer was 96779702119491.
"""

from __future__ import annotations
import dataclasses
import itertools
import math
import operator
import os
import typing


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


def part_one(path_to_input: str) -> int:
    equations = get_equations(path_to_input=path_to_input)
    return sum(
        equation.expected
        for equation in equations
        if equation.has_match(operators=(operator.add, operator.mul))
    )


def skip_slow(f):
    if os.environ.get("DO_SLOW") == "1":
        return f
    else:

        def inner(*args, **kwargs) -> str:
            return "<SKIPPED>"

        return inner


def concat(a: int, b: int) -> int:
    digits = int(math.log10(b) + 1)
    return (10**digits * a) + b


@skip_slow
def part_two(path_to_input: str) -> int:
    equations = get_equations(path_to_input=path_to_input)
    return sum(
        equation.expected
        for equation in equations
        if equation.has_match(
            operators=(operator.add, operator.mul, concat),
        )
    )


def main() -> int:
    print(part_one(path_to_input="07.input"))
    print(part_two(path_to_input="07.input"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
