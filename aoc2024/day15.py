from __future__ import annotations
import collections
import dataclasses
import aoc2024


@dataclasses.dataclass
class Coordinate:
    idx: int
    jdx: int

    def __hash__(self) -> int:
        return hash((self.idx, self.jdx))

    def __add__(self, other: Coordinate) -> Coordinate:
        return dataclasses.replace(
            self,
            idx=self.idx + other.idx,
            jdx=self.jdx + other.jdx,
        )

    def __sub__(self, other: Coordinate) -> Coordinate:
        return dataclasses.replace(
            self,
            idx=self.idx - other.idx,
            jdx=self.jdx - other.jdx,
        )


@dataclasses.dataclass
class State:
    boxes: set[Coordinate]
    moves: list[str]
    robot: Coordinate
    size: int
    walls: set[Coordinate]
    widen: bool

    @classmethod
    def from_path_to_input(cls, path_to_input: str, widen: bool) -> State:
        grid = collections.defaultdict(set)
        with open(file=path_to_input) as f:
            idx = 0
            for jdx, char in enumerate(f.readline().strip()):
                grid[char].add(Coordinate(idx=idx, jdx=jdx))
            size = jdx + 1
            for idx in range(1, size):
                for jdx, char in enumerate(f.readline().strip()):
                    grid[char].add(Coordinate(idx=idx, jdx=jdx))
            f.readline()
            moves = [char for line in f.readlines() for char in line.strip()]
        robot = grid["@"].pop()
        if widen:
            boxes = {dataclasses.replace(box, jdx=box.jdx * 2) for box in grid["O"]}
            robot = dataclasses.replace(robot, jdx=robot.jdx * 2)
            walls = {
                coordinate
                for wall in grid["#"]
                for coordinate in (
                    Coordinate(idx=wall.idx, jdx=wall.jdx * 2),
                    Coordinate(idx=wall.idx, jdx=wall.jdx * 2 + 1),
                )
            }
        else:
            boxes = grid["O"]
            walls = grid["#"]

        return cls(
            boxes=boxes,
            moves=moves,
            robot=robot,
            size=size,
            walls=walls,
            widen=widen,
        )

    def __str__(self) -> str:
        return "\n".join(
            "".join(
                "#"
                if (c := Coordinate(idx=idx, jdx=jdx)) in self.walls
                else "["
                if c in self.boxes
                else "@"
                if c == self.robot
                else "]"
                if c + self.MOVE_TO_DIRECTION["<"] in self.boxes
                else "."
                for jdx in range(self.size * 2 if self.widen else self.size)
            )
            for idx in range(self.size)
        )

    MOVE_TO_DIRECTION = {
        "^": Coordinate(-1, 0),
        ">": Coordinate(0, +1),
        "v": Coordinate(+1, 0),
        "<": Coordinate(0, -1),
    }

    def move(self, move: str) -> State:
        step = self.robot + (direction := self.MOVE_TO_DIRECTION[move])
        if step in self.walls:
            # robot hits the wall
            ...
        elif not self.widen and step in self.boxes:
            boxes = {step}
            while boxes:
                if (behind := boxes.pop() + direction) in self.walls:
                    # boxes are compacted against walls
                    break
                elif behind in self.boxes:
                    boxes.add(behind)
                else:
                    continue
            else:
                # robot pushes the boxes
                self.robot = step
                self.boxes.remove(step)
                self.boxes.add(behind)
        elif self.widen and (
            step in self.boxes
            or (left := step + self.MOVE_TO_DIRECTION["<"]) in self.boxes
        ):
            boxes = {step}
            if step in self.boxes:
                # The other half of the box is to its right
                boxes.add(step + self.MOVE_TO_DIRECTION[">"])
                to_move = {step}
            else:
                # The other half of the box is to its left
                boxes.add(left)
                to_move = {left}
            while boxes:
                if (behind := boxes.pop() + direction) in self.walls:
                    break
                elif (
                    behind in self.boxes
                    and behind + self.MOVE_TO_DIRECTION[">"] in self.walls
                ):
                    # boxes are compacted against walls
                    break
                elif (
                    behind in self.boxes
                    and (right := behind + self.MOVE_TO_DIRECTION[">"])
                    not in self.boxes
                ):
                    boxes.add(behind)
                    to_move.add(behind)
                    if move in "^v":
                        boxes.add(right)
                elif (
                    behind not in self.boxes
                    and (left := behind + self.MOVE_TO_DIRECTION["<"]) in self.boxes
                ):
                    boxes.add(behind)
                    if move not in "<>":
                        boxes.add(left)
                    to_move.add(left)
                else:
                    ...
            else:
                # robot pushes the boxes
                self.robot = step
                self.boxes -= to_move
                self.boxes.update({coordinate + direction for coordinate in to_move})
        else:
            # robot moves into open space
            self.robot = step
        return self


@aoc2024.expects(1398947)
def part_one(path_to_input: str) -> int:
    m = State.from_path_to_input(
        path_to_input=path_to_input,
        widen=False,
    )
    list(map(m.move, m.moves))
    return sum(100 * box.idx + box.jdx for box in m.boxes)


@aoc2024.expects(1397393)
def part_two(path_to_input: str) -> int:
    m = State.from_path_to_input(
        path_to_input=path_to_input,
        widen=True,
    )
    list(map(m.move, m.moves))
    return sum(100 * box.idx + box.jdx for box in m.boxes)
