import functools
import math
import aoc2024


@functools.lru_cache(maxsize=None)
def blink(depth: int, value: int) -> int:
    if depth == 0:
        return 1
    elif value == 0:
        return blink(depth=depth - 1, value=1)
    elif ((digits := int(math.log10(value)) + 1) % 2) == 0:
        return blink(depth=depth - 1, value=value // (10 ** (digits // 2))) + blink(
            depth=depth - 1,
            value=value % (10 ** (digits // 2)),
        )
    else:
        return blink(depth=depth - 1, value=value * 2024)


@aoc2024.expects(229043)
def part_one(path_to_input: str) -> int:
    with open(file=path_to_input) as f:
        stones = map(int, f.readline().split())
    return sum(blink(depth=25, value=value) for value in stones)


@aoc2024.expects(272673043446478)
def part_two(path_to_input: str) -> int:
    with open(file=path_to_input) as f:
        stones = map(int, f.readline().split())
    return sum(blink(depth=75, value=value) for value in stones)
