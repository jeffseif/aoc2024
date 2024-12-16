import collections

import more_itertools

import aoc2024


def read_column_ints(path_to_input: str) -> tuple[list[int], ...]:
    with open(file=path_to_input) as f:
        rows = (tuple(map(int, line.split())) for line in f)
        columns = more_itertools.unzip(rows)
        return tuple(map(list, columns))


@aoc2024.expects(2086478)
def part_one(path_to_input: str) -> int:
    lefts, rights = map(sorted, read_column_ints(path_to_input=path_to_input))
    distances = (abs(left - right) for left, right in zip(lefts, rights, strict=True))
    return sum(distances)


@aoc2024.expects(24941624)
def part_two(path_to_input: str) -> int:
    lefts, rights = map(
        collections.Counter, read_column_ints(path_to_input=path_to_input)
    )
    scores = (left * count * rights.get(left, 0) for left, count in lefts.items())
    return sum(scores)
