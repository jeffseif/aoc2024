import dataclasses
import typing

import aoc2024


HeightType = tuple[int, ...]


@dataclasses.dataclass
class Puzzle:
    keys: list[HeightType]
    locks: list[HeightType]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        keys: list[HeightType] = []
        locks: list[HeightType] = []

        def count_hashes(chars: list[str]) -> int:
            return sum(char == "#" for char in chars)

        with open(file=path_to_input) as f:
            for chunk in f.read().split("\n\n"):
                if chunk[:5] == "#" * 5:
                    collection = locks
                else:
                    collection = keys
                heights = tuple(map(count_hashes, zip(*chunk.splitlines()[1:-1])))  # type: ignore
                collection.append(heights)

        return cls(keys=keys, locks=locks)


# @aoc2024.expects(3)
@aoc2024.expects(3466)
def part_one(path_to_input: str) -> int:
    puzzle = Puzzle.from_path_to_input(path_to_input=path_to_input)
    return aoc2024.count(
        True
        for lock in puzzle.locks
        for key in puzzle.keys
        if all(l + k <= 5 for l, k in zip(lock, key))  # noqa
    )


@aoc2024.expects(0)
def part_two(path_to_input: str) -> int:
    return 0
