from __future__ import annotations
import dataclasses
import itertools
import typing
import aoc2024


@dataclasses.dataclass
class State:
    a: int
    b: int
    c: int
    program: list[int]
    output: list[int] = dataclasses.field(default_factory=list)
    idx: int = 0

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> State:
        with open(file=path_to_input) as f:
            _, _, a = f.readline().rpartition(" ")
            _, _, b = f.readline().rpartition(" ")
            _, _, c = f.readline().rpartition(" ")
            f.readline()
            _, _, program = f.readline().rpartition(" ")
            return cls(
                a=int(a),
                b=int(b),
                c=int(c),
                program=list(map(int, program.split(","))),
            )

    @property
    def iter_instruction_operand(self) -> typing.Iterator[tuple[int, int]]:
        while self.idx < len(self.program):
            yield self.program[self.idx], self.program[self.idx + 1]

    def combo(self, operand: int) -> int:
        return {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: self.a,
            5: self.b,
            6: self.c,
        }[operand]

    def step(self, instruction: int, operand: int) -> State:
        if instruction == 0:
            # adv
            self.a //= 1 << self.combo(operand=operand)
        elif instruction == 1:
            # bxl
            self.b ^= operand
        elif instruction == 2:
            # bst
            self.b = self.combo(operand=operand) % 8
        elif instruction == 3:
            # jnz
            if self.a == 0:
                ...
            else:
                self.idx = operand - 2
        elif instruction == 4:
            # bxc
            self.b ^= self.c
        elif instruction == 5:
            # out
            self.output.append(self.combo(operand) % 8)
        elif instruction == 6:
            # bdv
            self.b = self.a // (1 << self.combo(operand=operand))
        elif instruction == 7:
            # cdv
            self.c = self.a // (1 << self.combo(operand=operand))
        self.idx += 2
        return self

    def __str__(self) -> str:
        return ",".join(map(str, self.output))


@aoc2024.expects("2,1,0,4,6,2,4,2,0")
def part_one(path_to_input: str) -> str:
    state = State.from_path_to_input(path_to_input=path_to_input)
    list(itertools.starmap(state.step, state.iter_instruction_operand))
    return str(state)


@aoc2024.expects(0o3074103313322340)
def part_two(path_to_input: str) -> int:
    original = State.from_path_to_input(path_to_input=path_to_input)
    a = 1 << (3 * 15)
    for idx in reversed(range(len(original.program) - 1)):
        while True:
            state = dataclasses.replace(original, a=a, output=[])
            list(itertools.starmap(state.step, state.iter_instruction_operand))
            if state.output[idx:] == state.program[idx:]:
                break
            a += 1 << 3 * idx
    return a
