from __future__ import annotations
from collections import deque
from typing import List, Deque


class Node:
    def __init__(self, city: str) -> None:
        self.city = city
        self.children: List[Node] = []

    def add(self, city: str) -> None:
        self.children.append(Node(city))

    def bfs(self, queue: Deque[Node], city: str) -> bool:
        if self.city == city:
            return True

        for node in self.children:
            queue.append(node)

        try:
            node = queue.popleft()
            return node.bfs(queue, city)
        except IndexError:
            return False

    def aux_repr(self, depth: int) -> str:
        return (
            depth * "  "
            + self.city
            + "\n"
            + "".join(node.aux_repr(depth + 1) for node in self.children)
        )


class Tree:
    def __init__(self, root_city: str) -> None:
        self.root = Node(root_city)

    def add(self, city: str, depth: List[int]) -> bool:
        curr = self.root
        for i in depth:
            try:
                curr = curr.children[i]
            except IndexError:
                return False

        curr.add(city)
        return True

    def search(self, city: str) -> bool:
        return self.root.bfs(deque(), city)

    def __repr__(self) -> str:
        return self.root.aux_repr(0)


if __name__ == "__main__":
    mapa = Tree("Goiânia")
    mapa.add("Anápolis", [])
    mapa.add("Senador Canedo", [])
    mapa.add("Aparecida de Goiânia", [0])
    mapa.add("Abadia de Goiás", [0])
    mapa.add("Valparaíso", [1])
    mapa.add("Brasília", [1])
    mapa.add("Trindade", [0, 1])

    print(mapa)

    for city in [
        "Goiânia",
        "Anápolis",
        "Senador Canedo",
        "Aparecida de Goiânia",
        "Abadia de Goiás",
        "Valparaíso",
        "Brasília",
        "Trindade",
        "Trindade2",
    ]:
        if mapa.search(city):
            print(f"A cidade {city} foi encontrada")
        else:
            print(f"Não foi possível encontrar a cidade {city}")