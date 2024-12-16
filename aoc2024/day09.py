from __future__ import annotations
import dataclasses
import typing

import aoc2024


@dataclasses.dataclass
class Node:
    value: int | None
    width: int
    left: Node | None = None
    right: Node | None = None

    def __iter__(self) -> typing.Iterator[Node]:
        node: Node | None = self
        while node is not None:
            yield node
            node = node.right

    def __str__(self) -> str:
        return "".join(
            (str(node.value) if node.value is not None else ".") * node.width
            for node in self
        )


def compress(head: Node, tail: Node) -> None:
    left, right = next(node for node in head if node.value is None), tail
    while right.left is not None:
        if left == right:
            if (
                (head := next(node for node in head if node.value is None))
                == left
                == right
            ):
                break
            else:
                left, right = head, right.left
        elif left.value is not None:
            left: Node = left.right  # type:ignore[no-redef]
        elif right.value is None:
            right: Node = right.left  # type:ignore[no-redef]
        elif left.width == right.width:
            left.value, right.value = right.value, left.value
        elif left.width > right.width:
            # l <-> v <-> l.r
            void = Node(
                value=None,
                width=left.width - right.width,
                left=left,
                right=left.right,
            )
            if left.right is not None:
                left.right.left = void
            left.right = void

            # swap left/right
            left.value, left.width, right.value = (right.value, right.width, left.value)
        else:
            left: Node = left.right  # type:ignore[no-redef]
    return None


@aoc2024.expects(6378826667552)
def part_one(path_to_input: str) -> int:
    with open(file=path_to_input) as f:
        widths = list(map(int, f.read().strip()))

    head = tail = None
    for idx, width in enumerate(widths, start=1):
        for _ in range(width):
            node = Node(None if (idx % 2) == 0 else idx // 2, width=1)
            if head is None:
                head = node
            if tail is None:
                tail = head
            else:
                tail.right, node.left = node, tail
                tail = node

    assert head is not None
    assert tail is not None
    compress(head=head, tail=tail)

    return sum(
        idx * node.value for idx, node in enumerate(head) if node.value is not None
    )


@aoc2024.skip_slow
@aoc2024.expects(6413328569890)
def part_two(path_to_input: str) -> int:
    with open(file=path_to_input) as f:
        widths = list(map(int, f.read().strip()))

    head = tail = None
    for idx, width in enumerate(widths, start=1):
        node = Node(None if (idx % 2) == 0 else idx // 2, width=width)
        if head is None:
            head = node
        if tail is None:
            tail = head
        else:
            tail.right, node.left = node, tail
            tail = node

    assert head is not None
    assert tail is not None
    compress(head=head, tail=tail)

    return sum(
        idx * node.value
        for idx, node in enumerate(node for node in head for _ in range(node.width))
        if node.value is not None
    )
