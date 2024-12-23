from __future__ import annotations
import dataclasses
import itertools
import typing
import more_itertools

import aoc2024


class NoSolutionException(Exception): ...


@dataclasses.dataclass
class Machine:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int

    @classmethod
    def from_lines(cls, *lines: list[str]) -> Machine:
        (_, _, ax, ay), (_, _, bx, by), (_, px, py) = map(str.split, lines)  # type: ignore
        return cls(
            ax=int(ax[2:-1]),
            ay=int(ay[2:]),
            bx=int(bx[2:-1]),
            by=int(by[2:]),
            px=int(px[2:-1]),
            py=int(py[2:]),
        )

    def get_pushes(self, offset: int) -> tuple[int, int]:
        if self.ax * self.by - self.ay * self.bx == 0:
            raise NoSolutionException("Matrix is singular")
        else:
            x0_numer, x0_denom = (
                ((self.py + offset) * self.bx - (self.px + offset) * self.by),
                (self.ay * self.bx - self.ax * self.by),
            )
            if x0_numer % x0_denom:
                raise NoSolutionException(
                    f"{x0_numer=:}/{x0_denom=:} is not a round number"
                )
            x0 = x0_numer // x0_denom

            x1_numer, x1_denom = (self.px + offset - x0 * self.ax), self.bx
            if x1_numer % x1_denom:
                raise NoSolutionException(
                    f"{x1_numer=:}/{x1_denom=:} is not a round number"
                )
            x1 = x1_numer // x1_denom
            return x0, x1


def get_machines(path_to_input: str) -> typing.Iterable[Machine]:
    with open(file=path_to_input) as f:
        lines = filter(bool, map(str.strip, f.readlines()))
    return itertools.starmap(Machine.from_lines, more_itertools.chunked(lines, n=3))


@aoc2024.expects(29517)
def part_one(path_to_input: str) -> int:
    machines = get_machines(path_to_input=path_to_input)
    pushes = more_itertools.map_except(
        lambda m: m.get_pushes(offset=0),
        machines,
        NoSolutionException,
    )
    return sum(3 * a + b for a, b in pushes)


@aoc2024.expects(103570327981381)
def part_two(path_to_input: str) -> int:
    machines = get_machines(path_to_input=path_to_input)
    pushes = more_itertools.map_except(
        lambda m: m.get_pushes(offset=10_000_000_000_000),
        machines,
        NoSolutionException,
    )

    return sum(3 * a + b for a, b in pushes)
