import typing

import more_itertools


def iter_row(path_to_input: str) -> typing.Iterator[tuple[int, ...]]:
    with open(file=path_to_input) as f:
        for line in f:
            yield tuple(map(int, line.split()))


def is_safe(it: typing.Iterable[int]) -> bool:
    return (it_set := set(it)).issubset({1, 2, 3}) or it_set.issubset({-1, -2, -3})


def iter_diff(it: typing.Iterable[int]) -> typing.Iterator[int]:
    for left, right in more_itertools.pairwise(it):
        yield left - right


def part_one(path_to_input: str) -> int:
    safe = 0
    for row in iter_row(path_to_input=path_to_input):
        safe += is_safe(iter_diff(row))
    return safe


def part_two(path_to_input: str) -> int:
    safe = 0
    for row in iter_row(path_to_input=path_to_input):
        safe += is_safe(iter_diff(row)) or any(
            is_safe(iter_diff((*row[:idx], *row[idx + 1 :]))) for idx in range(len(row))
        )
    return safe


def main() -> int:
    print(part_one(path_to_input="02.input"))
    print(part_two(path_to_input="02.input"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
