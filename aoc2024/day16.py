from __future__ import annotations
import collections
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

    def __add__(self, other: Coordinate) -> Coordinate:
        return dataclasses.replace(
            self,
            idx=self.idx + other.idx,
            jdx=self.jdx + other.jdx,
        )

    def __lt__(self, other: Coordinate) -> bool:
        return self.idx < other.idx or self.jdx > other.idx


NORTH = Coordinate(idx=-1, jdx=0)
EAST = Coordinate(idx=0, jdx=+1)
SOUTH = Coordinate(idx=+1, jdx=0)
WEST = Coordinate(idx=0, jdx=-1)


LEFT_TURN = {
    NORTH: WEST,
    WEST: SOUTH,
    SOUTH: EAST,
    EAST: NORTH,
}
RIGHT_TURN = {v: k for k, v in LEFT_TURN.items()}
DIR_TO_STR = {
    NORTH: "^",
    WEST: "<",
    SOUTH: "v",
    EAST: ">",
}


def show(coords: set[Coordinate]) -> str:
    size = max(max(_.idx, _.jdx) for _ in coords) + 1
    return "\n".join(
        "".join("o" if Coordinate(idx, jdx) in coords else " " for jdx in range(size))
        for idx in range(size)
    )


def iter_score_path(
    path_to_input: str,
) -> typing.Iterator[tuple[int, list[Coordinate]]]:
    with open(file=path_to_input) as f:
        char_to_coords = collections.defaultdict(set)
        for idx, line in enumerate(f.readlines()):
            for jdx, char in enumerate(line.strip()):
                char_to_coords[char].add(Coordinate(idx=idx, jdx=jdx))
    heap = [(0, [char_to_coords["S"].pop()], EAST)]
    paths = char_to_coords["."]
    tail = char_to_coords["E"].pop()
    seen = set()
    while True:
        try:
            score, path, dir = heapq.heappop(heap)
        except IndexError:
            return
        node = path[-1]
        if node == tail:
            yield score, path
        else:
            for turn, margin in (
                (dir, 1),
                (LEFT_TURN[dir], 1001),
                (RIGHT_TURN[dir], 1001),
            ):
                if ((step := node + turn), turn) not in seen and (
                    step == tail or step in paths
                ):
                    heapq.heappush(heap, (score + margin, path + [step], turn))
        seen.add((node, dir))


@aoc2024.skip_slow
@aoc2024.expects(102488)
def part_one(path_to_input: str) -> int:
    score, _ = next(iter_score_path(path_to_input=path_to_input))
    return score


@aoc2024.skip_slow
@aoc2024.expects(559)
def part_two(path_to_input: str) -> int:
    lowest_score = float("inf")
    best_paths = set()
    for score, path in iter_score_path(path_to_input=path_to_input):
        if score <= lowest_score:
            best_paths.update(path)
        else:
            break
    return len(best_paths)
