import collections
import collections.abc
import itertools

import more_itertools

import aoc2024


def iter_code(path_to_input: str) -> collections.abc.Iterator[str]:
    with open(file=path_to_input) as f:
        yield from map(str.strip, f)


CHUNK_CACHE: dict[str, list[set[str]]] = {}


class Pad:
    COORDINATES: dict[str, tuple[int, int]]

    @classmethod
    def get_edges(cls) -> dict[str, dict[str, str]]:
        return {
            start: {
                ("<" if x2 < x1 else ">" if x1 < x2 else "v" if y1 < y2 else "^"): end
                for end, (x2, y2) in cls.COORDINATES.items()
                if (x1 == x2 and abs(y2 - y1) == 1) or (abs(x2 - x1) == 1 and y1 == y2)
            }
            for start, (x1, y1) in cls.COORDINATES.items()
        }

    @classmethod
    def get_paths_for_pair(cls, start: str, end: str) -> set[str]:
        edges = cls.get_edges()

        def iter_path(
            start: str, path: str, seen: tuple[str, ...]
        ) -> collections.abc.Iterator[str]:
            for dir, child in edges[start].items():
                if child in seen:
                    continue
                elif child == end:
                    yield path + dir
                else:
                    yield from iter_path(
                        start=child,
                        path=path + dir,
                        seen=(*seen, start),
                    )

        length_to_paths = collections.defaultdict(set)
        for path in iter_path(start=start, path="", seen=()):
            length_to_paths[len(path)].add(path)
        return {
            path
            for length, paths in itertools.islice(sorted(length_to_paths.items()), 1)
            for path in paths
        }

    @classmethod
    def get_paths_for_chunk(cls, chunk: str) -> list[set[str]]:
        if chunk not in CHUNK_CACHE:
            CHUNK_CACHE[chunk] = [
                cls.get_paths_for_pair(start=start, end=end)
                for start, end in itertools.pairwise("A" + chunk)
            ]
        return CHUNK_CACHE[chunk]

    @classmethod
    def iter_paths_for_sequence(cls, seq: str) -> collections.abc.Iterator[str]:
        multipaths = (
            paths
            for chunk in more_itertools.split_after(seq, "A".__eq__)
            for paths in cls.get_paths_for_chunk(chunk="".join(chunk))
        )
        interleaved = more_itertools.interleave(multipaths, itertools.cycle("A"))
        collapsed = filter(bool, interleaved)
        yield from map("".join, itertools.product(*collapsed))


class NumberPad(Pad):
    COORDINATES = {
        "7": (0, 0),
        "8": (1, 0),
        "9": (2, 0),
        "4": (0, 1),
        "5": (1, 1),
        "6": (2, 1),
        "1": (0, 2),
        "2": (1, 2),
        "3": (2, 2),
        "0": (1, 3),
        "A": (2, 3),
    }


class ArrowPad(Pad):
    COORDINATES = {
        "^": (1, 0),
        "<": (0, 1),
        ">": (2, 1),
        "A": (2, 0),
        "v": (1, 1),
    }


def accumulate_shortest_values(it: collections.abc.Iterator[str]) -> list[str]:
    ret: list[str] = []
    minimum = float("infinity")
    for s in it:
        if (length := len(s)) <= minimum:
            if length < minimum:
                ret.clear()
            ret.append(s)
            minimum = length
    return ret


def get_shortest_sequence(code: str, depth: int) -> str:
    current = 0
    seqs = list(NumberPad.iter_paths_for_sequence(seq=code))
    while current < depth:
        iter_paths = (
            path for seq in seqs for path in ArrowPad.iter_paths_for_sequence(seq=seq)
        )
        seqs = accumulate_shortest_values(it=iter_paths)
        current += 1
    else:
        return min(seqs, key=len)


def item_to_complexity(code: str, sequence: str) -> int:
    return int(code[:-1].lstrip("0")) * len(sequence)


@aoc2024.expects(213536)
def part_one(path_to_input: str) -> int:
    return sum(
        item_to_complexity(
            code=code, sequence=get_shortest_sequence(code=code, depth=2)
        )
        for code in iter_code(path_to_input=path_to_input)
    )


@aoc2024.skip_slow
@aoc2024.expects(258369757013802)
def part_two(path_to_input: str) -> int:
    return sum(
        item_to_complexity(
            code=code, sequence=get_shortest_sequence(code=code, depth=26)
        )
        for code in iter_code(path_to_input=path_to_input)
    )
