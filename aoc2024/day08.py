from __future__ import annotations
import collections
import dataclasses
import itertools
import typing
import aoc2024


@dataclasses.dataclass(order=True)
class Coordinate:
    idx: int
    jdx: int

    def harmonic(self, multiple: int, other: Coordinate) -> Coordinate:
        delta_idx, delta_jdx = (other.idx - self.idx), (other.jdx - self.jdx)
        return dataclasses.replace(
            self,
            idx=other.idx + multiple * delta_idx,
            jdx=other.jdx + multiple * delta_jdx,
        )

    def in_bounds(self, size: int) -> bool:
        return 0 <= self.idx < size and 0 <= self.jdx < size

    def __hash__(self) -> int:
        return hash((self.idx, self.jdx))


@dataclasses.dataclass
class AntennaGrid:
    coordinates: set[Coordinate]
    size: int

    @classmethod
    def from_tuples(cls, size: int, tuples: set[tuple[int, int]]) -> AntennaGrid:
        return cls(
            coordinates={Coordinate(idx=idx, jdx=jdx) for idx, jdx in tuples},
            size=size,
        )

    def iter_antinodes(
        self, multiples: typing.Iterable[int]
    ) -> typing.Iterator[Coordinate]:
        for left, right in itertools.permutations(self.coordinates, r=2):
            for multiple in multiples:
                if (
                    harmonic := left.harmonic(multiple=multiple, other=right)
                ).in_bounds(size=self.size):
                    yield harmonic


def get_freq_to_antenna_grid(path_to_input: str) -> dict[str, AntennaGrid]:
    freq_to_coords = collections.defaultdict(set)
    with open(file=path_to_input) as f:
        for idx, line in enumerate(map(str.strip, f)):
            size = len(line)
            for jdx, char in enumerate(line):
                if char not in ".#":
                    freq_to_coords[char].add((idx, jdx))
    return {
        freq: AntennaGrid.from_tuples(
            size=size,
            tuples=coords,
        )
        for freq, coords in freq_to_coords.items()
    }


@aoc2024.expects(222)
def part_one(path_to_input: str) -> int:
    freq_to_antenna_grid = get_freq_to_antenna_grid(path_to_input=path_to_input)
    antinodes = {
        antinode
        for antenna_grid in freq_to_antenna_grid.values()
        for antinode in antenna_grid.iter_antinodes(multiples=(1,))
    }
    return aoc2024.count(antinodes)


@aoc2024.expects(884)
def part_two(path_to_input: str) -> int:
    freq_to_antenna_grid = get_freq_to_antenna_grid(path_to_input=path_to_input)
    antinodes = {
        antinode
        for antenna_grid in freq_to_antenna_grid.values()
        for antinode in antenna_grid.iter_antinodes(
            multiples=range(0, antenna_grid.size)
        )
    }
    return aoc2024.count(antinodes)
