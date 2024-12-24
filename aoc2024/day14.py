from __future__ import annotations
import collections
import dataclasses
import functools
import operator
import typing
import aoc2024


@dataclasses.dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int

    @classmethod
    def from_line(cls, line: str) -> Robot:
        p, v = line.split()
        return cls(
            *map(int, p[2:].split(",")),
            *map(int, v[2:].split(",")),
        )

    def step(self, height: int, width: int) -> Robot:
        self.px = (self.px + self.vx) % width
        self.py = (self.py + self.vy) % height
        return self


def get_robots(path_to_input: str) -> list[Robot]:
    with open(file=path_to_input) as f:
        return list(map(Robot.from_line, f))


def show_robots(height: int, robots: list[Robot], width: int) -> str:
    positions = collections.Counter((robot.py, robot.px) for robot in robots)
    return "\n".join(
        "".join(
            str(positions[(idx, jdx)]) if (idx, jdx) in positions else "."
            for jdx in range(width)
        )
        for idx in range(height)
    )


def get_safety_factor(height: int, robots: list[Robot], width: int) -> int:
    positions = collections.Counter((robot.py, robot.px) for robot in robots)

    def get_count(idxs: typing.Iterable[int], jdxs: typing.Iterable[int]) -> int:
        return sum(positions.get((idx, jdx), 0) for idx in idxs for jdx in jdxs)

    return functools.reduce(
        operator.mul,
        (
            get_count(idxs=idxs, jdxs=jdxs)
            for idxs in (range(0, height // 2), range(height // 2 + 1, height))
            for jdxs in (range(0, width // 2), range(width // 2 + 1, width))
        ),
        1,
    )


def is_easter_egg(robots: list[Robot]) -> bool:
    positions = collections.Counter((robot.py, robot.px) for robot in robots)
    return max(positions.values()) == 1


@aoc2024.expects(221655456)
def part_one(path_to_input: str) -> int:
    robots = get_robots(path_to_input=path_to_input)
    height = max(robot.py for robot in robots) + 1
    width = max(robot.px for robot in robots) + 1
    for _ in range(100):
        [robot.step(height=height, width=width) for robot in robots]
    return get_safety_factor(height=height, robots=robots, width=width)


@aoc2024.expects(7858)
def part_two(path_to_input: str) -> int:
    robots = get_robots(path_to_input=path_to_input)
    height = max(robot.py for robot in robots) + 1
    width = max(robot.px for robot in robots) + 1

    steps = 0
    while not is_easter_egg(robots=robots):
        [robot.step(height=height, width=width) for robot in robots]
        steps += 1
    return steps
