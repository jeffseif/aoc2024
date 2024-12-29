from __future__ import annotations
import collections
import dataclasses
import typing
import aoc2024


@dataclasses.dataclass(frozen=True, slots=True)
class Coordinate:
    idx: int
    jdx: int

    def iter_neighbor(self, radius: int) -> typing.Iterator[tuple[int, Coordinate]]:
        for idx in range(-radius, radius + 1):
            for jdx in range(-radius, radius + 1):
                if 0 < (cheat_cost := abs(idx) + abs(jdx)) <= radius:
                    yield (
                        cheat_cost,
                        dataclasses.replace(
                            self,
                            idx=self.idx + idx,
                            jdx=self.jdx + jdx,
                        ),
                    )


@dataclasses.dataclass
class Track:
    end: Coordinate
    path: set[Coordinate]
    start: Coordinate
    walls: set[Coordinate]

    @classmethod
    def from_path_to_input(cls, path_input: str) -> Track:
        chars = collections.defaultdict(set)
        with open(file=path_input) as f:
            for idx, line in enumerate(f.readlines()):
                for jdx, char in enumerate(line.strip()):
                    chars[char].add(Coordinate(idx=idx, jdx=jdx))
        return cls(
            end=chars["E"].pop(),
            path=chars["."],
            start=chars["S"].pop(),
            walls=chars["#"],
        )

    def iter_savings(self, skip_distance: int) -> typing.Iterator[int]:
        step, depth = self.start, 1
        step_index = {step: depth}
        while step != self.end:
            # these are honest steps; work on them first so we populate
            # the cache for them
            (step,) = (
                neighbor
                for _, neighbor in step.iter_neighbor(radius=1)
                if (neighbor in self.path or neighbor == self.end)
                and neighbor not in step_index
            )
            depth += 1
            step_index[step] = depth
        yield 0
        for step, depth in step_index.items():
            for cheat_cost, neighbor in step.iter_neighbor(radius=skip_distance):
                if neighbor in self.path or neighbor == self.end:
                    if (savings := step_index[neighbor] - depth - cheat_cost) > 0:
                        yield savings


@aoc2024.expects(1286)
def part_one(path_to_input: str) -> int:
    track = Track.from_path_to_input(path_input=path_to_input)
    savings_to_count = collections.Counter(track.iter_savings(skip_distance=2))
    return sum(count for savings, count in savings_to_count.items() if savings >= 100)


@aoc2024.expects(989316)
def part_two(path_to_input: str) -> int:
    track = Track.from_path_to_input(path_input=path_to_input)
    savings_to_count = collections.Counter(track.iter_savings(skip_distance=20))
    return sum(count for savings, count in savings_to_count.items() if savings >= 100)
