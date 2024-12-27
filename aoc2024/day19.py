from __future__ import annotations
import collections
import dataclasses
import functools
import aoc2024


@dataclasses.dataclass
class State:
    designs: tuple[str, ...]
    patterns: set[str]

    def __hash__(self) -> int:
        return hash((self.designs, tuple(sorted(self.patterns))))

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> State:
        with open(file=path_to_input) as f:
            patterns = set(f.readline().strip().split(", "))
            f.readline()
            designs = tuple(map(str.strip, f.readlines()))
        return cls(
            designs=designs,
            patterns=patterns,
        )

    @functools.cached_property
    def max_pattern_length(self) -> int:
        return max(map(len, self.patterns))

    def has_match(self, design: str) -> bool:
        queue: collections.deque[tuple[tuple[str, ...], str]] = collections.deque(
            [((), design)]
        )
        seen = set()
        while queue:
            prefix, remaining = queue.popleft()
            if remaining in seen:
                continue
            elif not remaining:
                return True
            else:
                queue.extend(
                    (
                        prefix + (pattern,),
                        remaining[idx:],
                    )
                    for idx in range(
                        1, min(len(remaining), self.max_pattern_length) + 1
                    )
                    if (pattern := remaining[:idx]) in self.patterns
                )
            seen.add(remaining)
        else:
            return False

    @functools.cache
    def num_matches(self, design: str) -> int:
        if not design:
            # A match has been completed
            return 1
        else:
            return sum(
                self.num_matches(design=design[idx:])
                for idx in range(1, min(len(design), self.max_pattern_length) + 1)
                if design[:idx] in self.patterns
            )


@aoc2024.expects(240)
def part_one(path_to_input: str) -> int:
    state = State.from_path_to_input(path_to_input=path_to_input)
    return sum(map(state.has_match, state.designs))


@aoc2024.expects(848076019766013)
def part_two(path_to_input: str) -> int:
    state = State.from_path_to_input(path_to_input=path_to_input)
    return sum(map(state.num_matches, state.designs))
