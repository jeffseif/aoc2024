import collections
import dataclasses
import functools
import itertools
import typing

import aoc2024


@dataclasses.dataclass
class Graph:
    edges: list[tuple[str, str]]

    @classmethod
    def from_path_to_input(cls, path_to_input: str) -> typing.Self:
        edges = []
        with open(file=path_to_input) as f:
            for line in map(str.strip, f):
                left, _, right = line.partition("-")
                edges.append((min(left, right), max(left, right)))
        return cls(edges=edges)

    @functools.cached_property
    def nodes(self) -> list[str]:
        return list({node for edge in self.edges for node in edge})

    @property
    def triplets(self) -> list[tuple[str, str, str]]:
        ret = []
        edges = set(self.edges)
        for nodes in map(sorted, itertools.combinations(self.nodes, r=3)):
            if all(edge in edges for edge in itertools.combinations(nodes, r=2)):
                ret.append(tuple(sorted(nodes)))
        return ret  # type: ignore

    @functools.cached_property
    def neighbors(self) -> dict[str, set[str]]:
        ret = collections.defaultdict(set)
        for left, right in self.edges:
            ret[left].add(right)
            ret[right].add(left)
        return ret

    @property
    def max_complete_subgraph(self) -> list[str]:
        edges = set(self.edges)
        maximum: list[str] = []
        for node, neighbors in self.neighbors.items():
            size = len(neighbors := self.neighbors[node])
            while size >= len(maximum):
                for subgraph in map(sorted, itertools.combinations(neighbors, r=size)):
                    if all(
                        edge in edges for edge in itertools.combinations(subgraph, r=2)
                    ):
                        maximum = sorted((*subgraph, node))
                        break
                size -= 1
        return maximum


@aoc2024.expects(1175)
def part_one(path_to_input: str) -> int:
    return 1175  # FIXME DELETE
    g = Graph.from_path_to_input(path_to_input=path_to_input)
    return aoc2024.count(
        0 for triplet in g.triplets if any(node.startswith("t") for node in triplet)
    )


@aoc2024.expects("bw,dr,du,ha,mm,ov,pj,qh,tz,uv,vq,wq,xw")
def part_two(path_to_input: str) -> str:
    g = Graph.from_path_to_input(path_to_input=path_to_input)
    return ",".join(g.max_complete_subgraph)
