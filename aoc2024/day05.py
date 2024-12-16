import collections
import dataclasses
import itertools
import typing

import aoc2024


@dataclasses.dataclass
class OrdersAndUpdates:
    orders: dict[int, set[int]]
    updates: list[list[int]]


def get_orders_and_updates(path_to_input: str) -> OrdersAndUpdates:
    orders = collections.defaultdict(set)
    updates = []
    with open(file=path_to_input) as f:
        iter_line = map(str.strip, f.readlines())
        for line in iter_line:
            if not line:
                break
            before, after = map(int, line.split("|"))
            orders[before].add(after)
        for line in iter_line:
            updates.append(list(map(int, line.split(","))))
    return OrdersAndUpdates(
        orders=dict(orders),
        updates=updates,
    )


def get_middle(it: typing.Sequence[int]) -> int:
    return it[len(it) // 2]


@aoc2024.expects(4774)
def part_one(path_to_input: str) -> int:
    orders_and_updates = get_orders_and_updates(path_to_input=path_to_input)
    return sum(
        get_middle(it=update)
        for update in orders_and_updates.updates
        if all(
            before not in orders_and_updates.orders[after]
            for before, after in itertools.combinations(update, r=2)
        )
    )


def swap_sort(
    orders: dict[int, set[int]], update: typing.MutableSequence[int]
) -> typing.MutableSequence[int]:
    for idx, jdx in itertools.combinations(range(len(update)), r=2):
        if update[idx] in orders[update[jdx]]:
            update[idx], update[jdx] = update[jdx], update[idx]
    return update


@aoc2024.expects(6004)
def part_two(path_to_input: str) -> int:
    orders_and_updates = get_orders_and_updates(path_to_input=path_to_input)
    return sum(
        get_middle(it=swap_sort(orders=orders_and_updates.orders, update=update))
        for update in orders_and_updates.updates
        if any(
            before in orders_and_updates.orders[after]
            for before, after in itertools.combinations(update, r=2)
        )
    )
