from __future__ import annotations
import dataclasses
import itertools
import typing

import aoc2024


@dataclasses.dataclass
class Coordinate:
    idx: int
    jdx: int

    def __hash__(self) -> int:
        return hash((self.idx, self.jdx))


@dataclasses.dataclass
class Topo:
    heights: dict[Coordinate, int]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> Topo:
        with open(file=path_to_input) as f:
            return cls(
                heights={
                    Coordinate(idx=idx, jdx=jdx): int(char)
                    for idx, line in enumerate(f)
                    for jdx, char in enumerate(line.strip())
                },
            )

    def iter_step(self, coordinate: Coordinate) -> typing.Iterator[Coordinate]:
        for neighbor in (
            dataclasses.replace(coordinate, idx=coordinate.idx - 1),
            dataclasses.replace(coordinate, idx=coordinate.idx + 1),
            dataclasses.replace(coordinate, jdx=coordinate.jdx - 1),
            dataclasses.replace(coordinate, jdx=coordinate.jdx + 1),
        ):
            if (
                neighbor in self.heights
                and self.heights[neighbor] == self.heights[coordinate] + 1
            ):
                yield neighbor


@aoc2024.expects(531)
def part_one(path_to_input: str) -> int:
    topo = Topo.from_path_to_input(path_to_input=path_to_input)
    head_tails = set()
    for head in (
        coordinate for coordinate, height in topo.heights.items() if height == 0
    ):
        depth, iter_tail = 9, topo.iter_step(coordinate=head)
        while depth > 1:
            depth -= 1
            iter_tail = itertools.chain.from_iterable(map(topo.iter_step, iter_tail))
        for tail in iter_tail:
            head_tails.add((head, tail))
    return len(head_tails)


@aoc2024.expects(1210)
def part_two(path_to_input: str) -> int:
    topo = Topo.from_path_to_input(path_to_input=path_to_input)
    paths = set()
    for zero in (
        coordinate for coordinate, height in topo.heights.items() if height == 0
    ):
        for one in topo.iter_step(coordinate=zero):
            for two in topo.iter_step(coordinate=one):
                for three in topo.iter_step(coordinate=two):
                    for four in topo.iter_step(coordinate=three):
                        for five in topo.iter_step(coordinate=four):
                            for six in topo.iter_step(coordinate=five):
                                for seven in topo.iter_step(coordinate=six):
                                    for eight in topo.iter_step(coordinate=seven):
                                        for nine in topo.iter_step(coordinate=eight):
                                            paths.add(
                                                (
                                                    zero,
                                                    one,
                                                    two,
                                                    three,
                                                    four,
                                                    five,
                                                    six,
                                                    seven,
                                                    eight,
                                                    nine,
                                                )
                                            )
    return len(paths)
