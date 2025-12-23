import dataclasses
import enum
import operator
import typing

import aoc2024


class OP(enum.Enum):
    AND = operator.and_
    OR = operator.or_
    XOR = operator.xor


@dataclasses.dataclass(frozen=True)
class Gate:
    child: str
    op: OP
    parents: tuple[str, str]


@dataclasses.dataclass
class Puzzle:
    gates: dict[str, Gate]
    nodes: dict[str, bool | None]
    swapped: set[str] = dataclasses.field(default_factory=set)

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        nodes: dict[str, bool | None] = {}
        gates: dict[str, Gate] = {}
        with open(file=path_to_input) as f:
            for line in map(str.strip, f):
                if line:
                    id, _, value = line.partition(": ")
                    nodes[id] = bool(int(value))
                else:
                    break
            for line in map(str.strip, f):
                parent_op_parent, _, child = line.partition(" -> ")
                parent1, op, parent2 = parent_op_parent.split()
                for id in (child, parent1, parent2):
                    if id not in nodes:
                        nodes[id] = None
                gates[child] = Gate(
                    child=child,
                    op=OP[op],
                    parents=(
                        parent1,
                        parent2,
                    ),
                )
        return cls(
            gates=gates,
            nodes=nodes,
        )

    def __next__(self) -> None:
        while any(value is None for value in self.nodes.values()):
            for child, gate in self.gates.items():
                if self.nodes[child] is None:
                    if all(self.nodes[parent] is not None for parent in gate.parents):
                        self.nodes[child] = gate.op.value(
                            *(self.nodes[parent] for parent in gate.parents)
                        )
        raise StopIteration

    def __iter__(self) -> typing.Self:
        return self

    def get_int(self, prefix: str) -> int:
        bits = (
            value
            for id, value in sorted(self.nodes.items())
            if id.startswith(prefix)
            if value is not None
        )
        return sum(value << bit for bit, value in enumerate(bits))

    def with_swap(self, left: str, right: str) -> typing.Self:
        self.gates[right], self.gates[left] = (
            dataclasses.replace(self.gates[left], child=right),
            dataclasses.replace(self.gates[right], child=left),
        )
        self.swapped.update({left, right})
        return self


# @aoc2024.expects(2024)
@aoc2024.expects(49574189473968)
def part_one(path_to_input: str) -> int:
    puzzle = Puzzle.from_path_to_input(path_to_input=path_to_input)
    aoc2024.exhaust(puzzle)
    return puzzle.get_int(prefix="z")


@aoc2024.expects("ckb,kbs,ksv,nbd,tqq,z06,z20,z39")
def part_two(path_to_input: str) -> str:
    puzzle = (
        Puzzle.from_path_to_input(path_to_input=path_to_input)
        # Found through lots of trail and error :sweat:
        .with_swap(left="z06", right="ksv")
        .with_swap(left="z20", right="tqq")
        .with_swap(left="z39", right="ckb")
        .with_swap(left="kbs", right="nbd")
    )
    aoc2024.exhaust(puzzle)

    assert (
        diff := puzzle.get_int("x") + puzzle.get_int("y") - puzzle.get_int("z")
    ) == 0, bin(diff)

    return ",".join(sorted(puzzle.swapped))
