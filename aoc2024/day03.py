import itertools
import operator
import re
import typing


PATTERN = re.compile(r"mul\((\d+),(\d+)\)")


def iter_multiples(path_to_input: str) -> typing.Iterator[tuple[int, ...]]:
    with open(file=path_to_input) as f:
        for match in PATTERN.finditer(string=f.read()):
            yield tuple(map(int, match.groups()))


def part_one(path_to_input: str) -> int:
    products = itertools.starmap(
        operator.mul,
        iter_multiples(path_to_input=path_to_input),
    )
    return sum(products)


def iter_conditional_multiples(path_to_input: str) -> typing.Iterator[tuple[int, ...]]:
    with open(file=path_to_input) as f:
        payload = f.read()
    for dos in payload.split("do()"):
        without_dont, _, _ = dos.partition("don't()")
        for match in PATTERN.finditer(string=without_dont):
            yield tuple(map(int, match.groups()))


def part_two(path_to_input: str) -> int:
    products = itertools.starmap(
        operator.mul,
        iter_conditional_multiples(path_to_input=path_to_input),
    )
    return sum(products)
