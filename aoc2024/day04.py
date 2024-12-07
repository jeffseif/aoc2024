from __future__ import annotations
import dataclasses
import functools
import itertools
import re
import typing

import aoc2024


@dataclasses.dataclass
class Input:
    payload: str
    width: int

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> Input:
        with open(file=path_to_input) as f:
            payload = f.read()
        return cls(
            payload=payload,
            width=len(next(iter(payload.splitlines()))),
        )


def iter_pattern_one(width: int) -> typing.Iterator[str]:
    for delimeter in (
        # HORIZONTAL
        "",
        # RIGHT
        f".{{{2 * width:d}}}",
        # EVEN
        f".{{{2 * width - 1:d}}}",
        # LEFT
        f".{{{2 * width - 2:d}}}",
    ):
        yield delimeter.join("XMAS")
        yield delimeter.join("SAMX")


def iter_re_overlapping(
    pattern: str,
    string: str,
) -> typing.Iterator[str]:
    pat = re.compile(pattern=pattern)
    idx = 0
    while True:
        if (match := pat.search(string=string[idx:])) is None:
            return
        else:
            idx += match.start() + 1
            yield match.group()


def part_one(debug: bool, path_to_input: str) -> int:
    inp = Input.from_path_to_input(path_to_input=path_to_input)

    finditer = functools.partial(
        iter_re_overlapping,
        string=(" " * inp.width).join(inp.payload.splitlines()),
    )
    return aoc2024.count(
        itertools.chain(*map(finditer, iter_pattern_one(width=inp.width)))
    )


def iter_pattern_two(width: int) -> typing.Iterator[str]:
    middle = f"{{{2 * width - 2:d}}}A.{{{2 * width - 3:d}}}"
    for a, b, c, d in (
        # RIGHT
        ("M", "S", "M", "S"),
        # DOWN
        ("M", "M", "S", "S"),
        # LEFT
        ("S", "M", "S", "M"),
        # UP
        ("S", "S", "M", "M"),
    ):
        yield ".".join((a, b, middle, c, d))


def part_two(debug: bool, path_to_input: str) -> int:
    inp = Input.from_path_to_input(path_to_input=path_to_input)
    finditer = functools.partial(
        iter_re_overlapping,
        string=(" " * inp.width).join(inp.payload.splitlines()),
    )
    return aoc2024.count(
        itertools.chain(*map(finditer, iter_pattern_two(width=inp.width)))
    )
