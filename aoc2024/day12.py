from __future__ import annotations
import dataclasses
import typing
import aoc2024


@dataclasses.dataclass
class Coordinate:
    idx: int
    jdx: int

    def __hash__(self) -> int:
        return hash((self.idx, self.jdx))

    def __lt__(self, other: Coordinate) -> bool:
        return self.idx < other.idx or self.jdx < other.jdx

    def __add__(self, other: Coordinate) -> Coordinate:
        return dataclasses.replace(
            self,
            idx=self.idx + other.idx,
            jdx=self.jdx + other.jdx,
        )

    def __sub__(self, other: Coordinate) -> Coordinate:
        return self + -other

    def __neg__(self) -> Coordinate:
        return dataclasses.replace(
            self,
            idx=-self.idx,
            jdx=-self.jdx,
        )


@dataclasses.dataclass
class Garden:
    plots: dict[Coordinate, str]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> Garden:
        with open(file=path_to_input) as f:
            return cls(
                plots={
                    Coordinate(idx=idx, jdx=jdx): plot
                    for idx, line in enumerate(f)
                    for jdx, plot in enumerate(line.strip())
                }
            )
            return cls(plots=list(list(line.strip()) for line in f))

    def iter_neighbor(self, coordinate: Coordinate) -> typing.Iterator[Coordinate]:
        for neighbor in (
            dataclasses.replace(coordinate, idx=coordinate.idx - 1),
            dataclasses.replace(coordinate, idx=coordinate.idx + 1),
            dataclasses.replace(coordinate, jdx=coordinate.jdx - 1),
            dataclasses.replace(coordinate, jdx=coordinate.jdx + 1),
        ):
            if (
                neighbor in self.plots
                and self.plots[neighbor] == self.plots[coordinate]
            ):
                yield neighbor

    @property
    def iter_region(self) -> typing.Iterator[set[Coordinate]]:
        unseen = set(self.plots)
        while unseen:
            neighbors, region = {unseen.pop()}, set()
            while neighbors:
                coordinate = neighbors.pop()
                region.add(coordinate)
                for neighbor in self.iter_neighbor(coordinate=coordinate):
                    if neighbor not in region:
                        neighbors.add(neighbor)
            unseen -= region
            yield region

    def get_perimeter(self, coordinates: set[Coordinate]) -> int:
        edges = {
            (coordinate, neighbor)
            for coordinate in coordinates
            for neighbor in self.iter_neighbor(coordinate=coordinate)
        }
        return 4 * len(coordinates) - len(edges)

    DIRECTION_ROTATION_MAP = {
        Coordinate(+1, 0): Coordinate(0, -1),
        Coordinate(0, -1): Coordinate(-1, 0),
        Coordinate(-1, 0): Coordinate(0, +1),
        Coordinate(0, +1): Coordinate(+1, 0),
    }

    def get_sides(self, coordinates: set[Coordinate]) -> int:
        normals = {
            (coordinate, direction)
            for coordinate in coordinates
            for direction in self.DIRECTION_ROTATION_MAP
            # This is an edge
            if coordinate + direction not in coordinates
        }
        corners = 0
        for coordinate, direction in normals:
            corners += (
                coordinate + self.DIRECTION_ROTATION_MAP[direction],
                direction,
            ) not in normals
            corners += (
                coordinate - self.DIRECTION_ROTATION_MAP[direction],
                direction,
            ) not in normals
        # we double-count the corners
        return corners // 2


@aoc2024.expects(1450816)
def part_one(path_to_input: str) -> int:
    garden = Garden.from_path_to_input(path_to_input=path_to_input)
    return sum(
        len(region) * garden.get_perimeter(coordinates=region)
        for region in garden.iter_region
    )


@aoc2024.expects(865662)
def part_two(path_to_input: str) -> int:
    garden = Garden.from_path_to_input(path_to_input=path_to_input)
    return sum(
        len(region) * garden.get_sides(coordinates=region)
        for region in garden.iter_region
    )
