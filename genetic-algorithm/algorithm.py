from random import random, sample
from typing import Dict, List, Set, Tuple

# from itertools import filterfalse


class Genetic:
    def __init__(
        self,
        individuals: int,
        genes: int,
        upper_limit: float,
        lower_limit: float,
    ) -> None:
        self._individuals = individuals
        self._genes = genes
        self._upper_limit = upper_limit
        self._lower_limit = lower_limit
        self.population: Dict[str, List[float]] = self._create_population()

    def _create_individual(self) -> List[float]:
        return [self.random_range(self._upper_limit, self._lower_limit) for _ in range(self._genes)]

    def _create_population(self) -> Dict[str, List[float]]:
        return {str(i): self._create_individual() for i in range(self._individuals)}

    @staticmethod
    def random_range(upper_limit: float, lower_limit: float) -> float:
        return random() * (upper_limit - lower_limit) + lower_limit

    # Soma de genes
    def fitness(self, individual: List[float]) -> float:
        return sum(individual)

    # Roleta ponderada
    def _selection(self) -> Set[str]:
        population_fitness = {k: self.fitness(v) for k, v in self.population.items()}
        raw_roulette = {
            item[0]: item[1] for item in sorted(population_fitness.items(), key=lambda item: item[1], reverse=True)
        }

        selected_individuals: Set[str] = set()

        for _ in range(self._individuals // 2):
            total_sum = sum(v for _, v in raw_roulette.items())
            roulette = map(lambda item: (item[0], item[1] / total_sum * 100), raw_roulette.items())

            random_individual = self.random_range(100, 0)

            for (k, v) in roulette:
                random_individual -= v
                if random_individual <= 0:
                    raw_roulette.pop(k)
                    selected_individuals.add(k)
                    break

        return selected_individuals

    # Pareamento aleatório
    def _pairing(self, selected_individuals: Set[str]) -> Set[Tuple[str, str]]:
        parents_set: Set[Tuple[str, str]] = set()

        while len(selected_individuals) >= 2:
            selected_pair = (selected_individuals.pop(), selected_individuals.pop())
            parents_set.add(selected_pair)

        return parents_set

    # Cruzamento em dois pontos
    def _mating(self, parents_set: Set[Tuple[str, str]]):

        for parents in parents_set:
            mating_points = sorted(sample(range(self._genes), k=2))

            genes1 = self.population[parents[0]]
            genes2 = self.population[parents[1]]

            child1 = genes1[:]
            child2 = genes2[:]
            for i, point in enumerate(mating_points):
                if i % 2 == 0:
                    child1 = child1[:point] + genes2[point:]
                    child2 = child2[:point] + genes1[point:]
                else:
                    child1 = child1[:point] + genes1[point:]
                    child2 = child2[:point] + genes2[point:]


if __name__ == "__main__":

    g = Genetic(10, 5, 5, -5)
    # print(g.population)
    # print(g.population.items())
    selected = g._selection()
    print(selected, end="\n\n")
    parents = g._pairing(selected)
    print(parents, end="\n\n")
    g._mating(parents)
    # print(sum(v for (_, v) in roulette))
