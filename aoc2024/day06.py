from __future__ import annotations
import dataclasses
import itertools
import time
import typing
import aoc2024


@dataclasses.dataclass(order=True, unsafe_hash=True)
class Coordinate:
    idx: int
    jdx: int


@dataclasses.dataclass
class State:
    blocks: tuple[tuple[bool, ...], ...]
    direction: Coordinate
    position: Coordinate

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> State:
        with open(file=path_to_input) as f:
            blocks_lines, position_lines = itertools.tee(f, 2)

            return cls(
                blocks=tuple(
                    tuple(char == "#" for char in line.strip()) for line in blocks_lines
                ),
                direction=Coordinate(-1, 0),
                position=next(
                    Coordinate(idx=idx, jdx=jdx)
                    for idx, row in enumerate(position_lines)
                    for jdx, char in enumerate(row)
                    if char == "^"
                ),
            )

    def __next__(self) -> State:
        return dataclasses.replace(
            self,
            position=dataclasses.replace(
                self.position,
                idx=self.position.idx + self.direction.idx,
                jdx=self.position.jdx + self.direction.jdx,
            ),
        )

    def __len__(self) -> int:
        return len(self.blocks)

    @property
    def is_escaped(self) -> bool:
        return (
            self.position.idx < 0
            or self.position.idx >= len(self)
            or self.position.jdx < 0
            or self.position.jdx >= len(self)
        )

    @property
    def is_blocked(self) -> bool:
        return self.blocks[self.position.idx][self.position.jdx]

    DIRECTION_ROTATION_MAP = {
        (+1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, +1),
        (0, +1): (+1, 0),
    }

    def rotate(self) -> None:
        idx, jdx = self.DIRECTION_ROTATION_MAP[(self.direction.idx, self.direction.jdx)]
        self.direction = dataclasses.replace(self.direction, idx=idx, jdx=jdx)

    DIRECTION_STR_MAP = {
        (-1, 0): "^",
        (0, +1): ">",
        (+1, 0): "v",
        (0, -1): "<",
    }

    def __str__(self) -> str:
        basemap = [["#" if blocked else " " for blocked in row] for row in self.blocks]
        basemap[self.position.idx][self.position.jdx] = self.DIRECTION_STR_MAP[
            (self.direction.idx, self.direction.jdx)
        ]
        return "\n" + "\n".join(" ".join(row) for row in basemap)

    def iter_coordinates(self, debug: bool) -> typing.Iterator[Coordinate]:
        seen = {self.position}
        while True:
            if (step := next(self)).is_escaped:
                break
            elif step.is_blocked:
                self.rotate()
            else:
                self = step
            seen.add(self.position)
            if debug:
                print(self)
                time.sleep(DELAY_SECONDS)
        yield from sorted(seen)

    def with_obstacle(self, obstacle: Coordinate) -> State:
        return dataclasses.replace(
            self,
            blocks=tuple(
                tuple(
                    True if jdx == obstacle.jdx else blocked
                    for jdx, blocked in enumerate(row)
                )
                if idx == obstacle.idx
                else row
                for idx, row in enumerate(self.blocks)
            ),
        )


DELAY_SECONDS = 0.005


def part_one(debug: bool, path_to_input: str) -> int:
    return aoc2024.count(
        State.from_path_to_input(path_to_input=path_to_input).iter_coordinates(
            debug=debug
        )
    )


@aoc2024.skip_slow
def part_two(debug: bool, path_to_input: str) -> int:
    unobstructed = State.from_path_to_input(path_to_input=path_to_input)
    loops = 0
    for obstacle in unobstructed.iter_coordinates(debug=debug):
        if debug:
            print(obstacle)
        obstructed = unobstructed.with_obstacle(obstacle=obstacle)
        seen = {(obstructed.position, obstructed.direction)}
        while True:
            if (step := next(obstructed)).is_escaped:
                break
            elif step.is_blocked:
                obstructed.rotate()
            elif (step.position, step.direction) in seen:
                loops += 1
                break
            else:
                obstructed = step
            seen.add((obstructed.position, obstructed.direction))
            if debug:
                print(obstructed)
                time.sleep(DELAY_SECONDS)
    return loops
