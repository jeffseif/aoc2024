from __future__ import annotations
import dataclasses
import heapq
import typing
import aoc2024


@dataclasses.dataclass
class Coordinate:
    idx: int
    jdx: int

    def __hash__(self) -> int:
        return hash((self.idx, self.jdx))

    def __lt__(self, other: Coordinate) -> bool:
        return self.idx > other.idx or self.jdx > other.jdx

    def iter_neighbor(self, size: int) -> typing.Iterator[Coordinate]:
        for idx, jdx in (
            (-1, 0),
            (0, +1),
            (+1, 0),
            (0, -1),
        ):
            if (0 <= self.idx + idx < size) and (0 <= self.jdx + jdx < size):
                yield dataclasses.replace(self, idx=self.idx + idx, jdx=self.jdx + jdx)


@dataclasses.dataclass
class State:
    size: int
    walls: list[Coordinate]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> State:
        with open(file=path_to_input) as f:
            walls = [
                Coordinate(*map(int, line.strip().split(","))) for line in f.readlines()
            ]
        size = max(max(coord.idx, coord.jdx) for coord in walls) + 1
        return cls(
            size=size,
            walls=walls,
        )

    def get_path(self, num_coords: int) -> list[Coordinate]:
        heap: list[tuple[int, Coordinate, list[Coordinate]]] = [
            (0, Coordinate(idx=0, jdx=0), [])
        ]
        goal = Coordinate(idx=self.size - 1, jdx=self.size - 1)
        seen = set()
        walls = set(self.walls[:num_coords])
        while heap:
            depth, step, path = heapq.heappop(heap)
            if step == goal:
                return path
            elif step in seen:
                continue
            else:
                for neighbor in step.iter_neighbor(size=self.size):
                    if neighbor not in walls:
                        heapq.heappush(heap, (depth + 1, neighbor, path + [step]))
                seen.add(step)
        else:
            raise ValueError


@aoc2024.expects(280)
def part_one(path_to_input: str) -> int:
    state = State.from_path_to_input(path_to_input=path_to_input)
    return len(state.get_path(num_coords=1024))


@aoc2024.expects("28,56")
def part_two(path_to_input: str) -> str:
    state = State.from_path_to_input(path_to_input=path_to_input)
    low, high = 0, 4000
    while high - low > 1:
        middle = (high + low) // 2
        try:
            state.get_path(num_coords=middle)
        except ValueError:
            high = middle
        else:
            low = middle
    else:
        corrupting_wall = state.walls[high - 1]
        return f"{corrupting_wall.idx:d},{corrupting_wall.jdx:d}"
