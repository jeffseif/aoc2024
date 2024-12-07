"""
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...
Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...
This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..
By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..
In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

Your puzzle answer was 5318.

--- Part Two ---
While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...
Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:


....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...
Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...
Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...
Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...
Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..
It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?

Your puzzle answer was 1831.
"""

from __future__ import annotations
import dataclasses
import itertools
import os
import time
import typing


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

    def iter_coordinates(self, display: bool) -> typing.Iterator[Coordinate]:
        seen = {self.position}
        while True:
            if (step := next(self)).is_escaped:
                break
            elif step.is_blocked:
                self.rotate()
            else:
                self = step
            seen.add(self.position)
            if display:
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


def count(it: typing.Iterable) -> int:
    count = 0
    for _ in it:
        count += 1
    return count


def part_one(display: bool, path_to_input: str) -> int:
    return count(
        State.from_path_to_input(path_to_input=path_to_input).iter_coordinates(
            display=display
        )
    )


def skip_slow(f):
    if os.environ.get("DO_SLOW") == "1":
        return f
    else:

        def inner(*args, **kwargs) -> str:
            return "<SKIPPED>"

        return inner


@skip_slow
def part_two(display: bool, path_to_input: str) -> int:
    unobstructed = State.from_path_to_input(path_to_input=path_to_input)
    loops = 0
    for obstacle in unobstructed.iter_coordinates(display=display):
        if display:
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
            if display:
                print(obstructed)
                time.sleep(DELAY_SECONDS)
    return loops


def main() -> int:
    print(part_one(display=False, path_to_input="06.input"))
    print(part_two(display=False, path_to_input="06.input"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
