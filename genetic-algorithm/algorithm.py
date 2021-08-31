from random import random
from types import FunctionType
from typing import Dict, List

# from itertools import filterfalse


class Genetic:
    def __init__(
        self, individuals: int, genes: int, upper_limit: float, lower_limit: float, fitness_func: FunctionType
    ) -> None:
        self._individuals = individuals
        self._genes = genes
        self._upper_limit = upper_limit
        self._lower_limit = lower_limit
        self._fitness_func = fitness_func
        self.population: Dict[int, List[float]] = self._create_population()

    def _create_individual(self) -> List[float]:
        return [self._random(self._upper_limit, self._lower_limit) for _ in range(self._genes)]

    def _create_population(self) -> Dict[int, List[float]]:
        return {i: self._create_individual() for i in range(self._individuals)}

    @classmethod
    def _random(cls, upper_limit: float, lower_limit: float) -> float:
        return random() * (upper_limit - lower_limit) + lower_limit

    def fitness(self, individual):
        return sum((self._fitness_func(gene) for gene in individual))

    def _weighted_roulette(self):
        population_fitness = {k: self.fitness(v) for k, v in self.population.items()}
        population_fitness_sorted = sorted(population_fitness.items(), key=lambda item: item[1])[::-1]

        selected_population = set()

        for _ in range(self._individuals // 2):
            population_fitness_sorted = list(
                filter(lambda item: item[0] not in selected_population, population_fitness_sorted)
            )
            total_sum = sum(v for (_, v) in population_fitness_sorted)
            roulette = map(lambda item: (item[0], item[1] / total_sum * 100), population_fitness_sorted)

            random_individual = self._random(100, 0)

            for (k, v) in roulette:
                random_individual -= v
                if random_individual <= 0:
                    selected_population.add(k)
                    break

        return selected_population


def func(x):
    return abs(-(x ** 2) + 16)


if __name__ == "__main__":

    g = Genetic(10, 5, 10, 1, func)
    # print(g.population)
    print(g.population.items())
    seleted = g._weighted_roulette()
    print(seleted)
    # print(sum(v for (_, v) in roulette))
