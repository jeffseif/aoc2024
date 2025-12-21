import collections
import collections.abc
import dataclasses
import itertools

import aoc2024


@dataclasses.dataclass
class RNG:
    secret: int
    changes: collections.deque = dataclasses.field(
        default_factory=lambda: collections.deque(maxlen=4)
    )
    changes_to_price: dict[tuple[int, int, int, int], int] = dataclasses.field(
        default_factory=dict
    )

    @staticmethod
    def mix_and_prune(left: int, right: int) -> int:
        return (left ^ right) % 16777216

    def __next__(self) -> int:
        new = self.secret
        new = self.mix_and_prune(left=new, right=new * 64)
        new = self.mix_and_prune(left=new, right=new // 32)
        new = self.mix_and_prune(left=new, right=new * 2048)
        self.changes.append((new % 10) - (self.secret % 10))
        self.secret = new
        if len(self.changes) == 4:
            key: tuple[int, int, int, int] = tuple(self.changes)
            if key not in self.changes_to_price:
                self.changes_to_price[key] = new % 10
        return new

    def __iter__(self) -> collections.abc.Iterator[int]:
        return self


def iter_rng(path_to_input: str) -> collections.abc.Iterator[RNG]:
    with open(file=path_to_input) as f:
        for secret in map(int, f):
            yield RNG(secret=secret)


@aoc2024.expects(16039090236)
def part_one(path_to_input: str) -> int:
    ret = 0
    for rng in iter_rng(path_to_input=path_to_input):
        aoc2024.exhaust(itertools.islice(rng, 2000))
        ret += rng.secret
    return ret


@aoc2024.expects(1808)
def part_two(path_to_input: str) -> int:
    changes_to_total: dict[tuple[int, int, int, int], int] = collections.defaultdict(
        int
    )
    for rng in iter_rng(path_to_input=path_to_input):
        aoc2024.exhaust(itertools.islice(rng, 2000))
        for changes, price in rng.changes_to_price.items():
            changes_to_total[changes] += price
    return max(changes_to_total.values())
