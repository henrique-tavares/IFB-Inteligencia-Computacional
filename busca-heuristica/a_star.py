from __future__ import annotations
from collections import defaultdict
from typing import Callable, Dict, List, NamedTuple, Set, Tuple
from time import time


class Edge(NamedTuple):
    city: str
    distance: int

    def __eq__(self, other: Edge) -> bool:
        return self.city == other.city

    def __hash__(self) -> int:
        return hash(self.city)


class Graph:
    def __init__(self) -> None:
        self.elements: Dict[str, Set[Edge]] = defaultdict(set)

    def __repr__(self) -> str:
        return (
            "{"
            + "; ".join(
                f"'{vertice}': " + ", ".join(f"('{edge.city}', {edge.distance}Km)" for edge in edges)
                for vertice, edges in self.elements.items()
            )
            + "}"
        )

    def __getitem__(self, item: str) -> Set[Edge]:
        return self.elements[item]

    def __setitem__(self, key, item: Set[Edge]) -> None:
        self.elements[key] = item

    def add(self, vertice: str, *edges: Edge, bidirectional: bool = False) -> None:
        self[vertice] |= set(edges)

        if bidirectional:
            for edge in edges:
                self.add(edge.city, Edge(vertice, edge.distance))

    def a_star(
        self,
        current: str,
        destination: str,
        heuristic: Callable[[str], int],
        cummulative_distance: int = 0,
        path: List[str] = None,
    ) -> Tuple[List[str], int]:
        if path is None:
            path = []

        path.append(current)

        if current == destination:
            return path, cummulative_distance

        next_vertice, cummulative_distance, _ = min(
            (
                (edge.city, cummulative_distance + edge.distance, heuristic(edge.city))
                for edge in self[current]
                if edge.city not in path
            ),
            key=lambda e: e[1] + e[2],
        )

        return self.a_star(next_vertice, destination, heuristic, cummulative_distance, path.copy())


def heuristic_outer() -> Callable[[str], int]:
    distance_table_to_bucharest = {
        "Arad": 366,
        "Bucharest": 0,
        "Craiova": 160,
        "Dobreta": 242,
        "Eforie": 161,
        "Fagaras": 178,
        "Giurgiu": 77,
        "Hirsova": 151,
        "Iasi": 226,
        "Lugoj": 244,
        "Mehadia": 241,
        "Neamt": 234,
        "Oradea": 380,
        "Pitesti": 98,
        "Rimnicu Vilcea": 193,
        "Sibiu": 253,
        "Timisoara": 329,
        "Urziceni": 80,
        "Vaslui": 199,
        "Zerind": 374,
    }

    def heuristic_inner(city: str) -> int:
        return distance_table_to_bucharest[city]

    return heuristic_inner


if __name__ == "__main__":
    g = Graph()

    g.add("Arad", Edge("Zerind", 75), Edge("Sibiu", 140), Edge("Timisoara", 118))
    g.add(
        "Bucharest",
        Edge("Pitesti", 101),
        Edge("Fagaras", 211),
        Edge("Urziceni", 85),
        Edge("Giurgiu", 90),
    )
    g.add(
        "Craiova",
        Edge("Dobreta", 120),
        Edge("Rimnicu Vilcea", 146),
        Edge("Pitesti", 138),
    )
    g.add("Dobreta", Edge("Mehadia", 75), Edge("Craiova", 120))
    g.add("Eforie", Edge("Hirsova", 86))
    g.add("Fagaras", Edge("Sibiu", 99), Edge("Bucharest", 211))
    g.add("Giurgiu", Edge("Bucharest", 90))
    g.add("Hirsova", Edge("Urziceni", 98), Edge("Eforie", 86))
    g.add("Iasi", Edge("Neamt", 87), Edge("Vaslui", 92))
    g.add("Lugoj", Edge("Timisoara", 111), Edge("Mehadia", 70))
    g.add("Mehadia", Edge("Lugoj", 70), Edge("Dobreta", 75))
    g.add("Neamt", Edge("Iasi", 87))
    g.add("Oradea", Edge("Sibiu", 151), Edge("Zerind", 71))
    g.add(
        "Pitesti",
        Edge("Bucharest", 101),
        Edge("Craiova", 138),
        Edge("Rimnicu Vilcea", 97),
    )
    g.add("Rimnicu Vilcea", Edge("Pitesti", 97), Edge("Craiova", 146), Edge("Sibiu", 80))
    g.add(
        "Sibiu",
        Edge("Fagaras", 99),
        Edge("Rimnicu Vilcea", 80),
        Edge("Arad", 140),
        Edge("Oradea", 151),
    )
    g.add("Timisoara", Edge("Arad", 118), Edge("Lugoj", 111))
    g.add("Urziceni", Edge("Vaslui", 142), Edge("Hirsova", 98), Edge("Bucharest", 85))
    g.add("Vaslui", Edge("Urziceni", 142), Edge("Iasi", 92))
    g.add("Zerind", Edge("Oradea", 71), Edge("Arad", 75))

    for vertice in g.elements:
        start = time()
        res = g.a_star(vertice, "Bucharest", heuristic_outer())
        finish = time()
        print(f"{((finish - start) * 1000):.2f}ms", f"({res[1]:3d}Km)", " -> ".join(city for city in res[0]))
