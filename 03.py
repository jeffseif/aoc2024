import itertools
import operator
import re
import typing


PATTERN = re.compile("mul\((\d+),(\d+)\)")


def iter_multiples(path_to_input: str) -> typing.Iterator[tuple[int, int]]:
    with open(file=path_to_input) as f:
        for match in PATTERN.finditer(string=f.read()):
            yield tuple(map(int, match.groups()))


def part_one(path_to_input: str) -> int:
    products = itertools.starmap(
        operator.mul,
        iter_multiples(path_to_input=path_to_input),
    )
    return sum(products)


def iter_conditional_multiples(path_to_input: str) -> typing.Iterator[tuple[int, int]]:
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


def main() -> int:
    print(part_one(path_to_input="03.input"))
    print(part_two(path_to_input="03.input"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
