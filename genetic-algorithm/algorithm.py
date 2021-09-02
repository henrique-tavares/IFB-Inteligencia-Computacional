from random import gauss, random, sample
from typing import Callable, Dict, List, Set, Tuple
import math as m


class Genetic:
    def __init__(
        self,
        individuals: int,
        genes: int,
        upper_limit: float,
        lower_limit: float,
        fitness_func: Callable[[float], float] = None,
    ) -> None:
        self._individuals = individuals
        self._genes = genes
        self._upper_limit = upper_limit
        self._lower_limit = lower_limit
        self._fitness_func = fitness_func
        self.population: Dict[str, List[float]] = self._create_population()

    def next_generation(self):
        # Seleção
        selected_individuals = self._selection()

        # Pareamento
        paired_parents = self._pairing(selected_individuals)

        # Cruzamento
        offsprings = list()
        for parents_pair in paired_parents:
            offsprings.extend(self._mating(parents_pair))

        # Mutação
        mutating_individuals = selected_individuals.copy()
        for i, offspring in enumerate(offsprings):
            self.population[str(i + self._individuals)] = offspring
            mutating_individuals.add(str(i + self._individuals))

        for individual in mutating_individuals:
            self._mutation(individual)

        # Nova Geração
        population_fitness = self._population_fitness()
        new_generation = {
            str(item[0]) for item in sorted(population_fitness.items(), key=lambda item: item[1], reverse=True)[:10]
        }

        self.population = {str(i): self.population[individual] for i, individual in enumerate(new_generation)}

    def _create_individual(self) -> List[float]:
        return [self.random_range(self._upper_limit, self._lower_limit) for _ in range(self._genes)]

    def _create_population(self) -> Dict[str, List[float]]:
        return {str(i): self._create_individual() for i in range(self._individuals)}

    # Soma de genes
    def _fitness(self, individual: List[float]) -> float:
        if self._fitness_func is None:
            return sum(individual)

        return self._fitness_func(sum(individual))

    def _population_fitness(self) -> Dict[str, float]:
        return {k: self._fitness(v) for k, v in self.population.items()}

    # Roleta ponderada
    def _selection(self) -> Set[str]:
        population_fitness = self._population_fitness()
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
    def _pairing(self, selected_individuals: Set[str], num_parents=2) -> Set[Tuple[str, ...]]:
        selected_individuals = selected_individuals.copy()
        paired_parents: Set[Tuple[str, ...]] = set()

        while len(selected_individuals) >= num_parents:
            selected_pair = tuple(selected_individuals.pop() for _ in range(num_parents))
            paired_parents.add(selected_pair)

        return paired_parents

    # Cruzamento em vários pontos (default: 2)
    def _mating(self, parents: Tuple[str, ...], num_points: int = 2) -> List[List[float]]:

        mating_points: List[int] = sorted(sample(range(self._genes), k=num_points))

        genes_list: List[List[float]] = [self.population[parent] for parent in parents]

        children: List[List[float]] = genes_list.copy()

        for i in range(len(children)):
            for j, point in enumerate(mating_points):
                children[i] = children[i][:point] + genes_list[(i + j + 1) % len(genes_list)][point:]

        return children

    # Mutação gaussiana
    def _mutation(self, individual: str, mutation_rate: int = 1) -> None:
        mutating_points = sample(range(self._genes), k=mutation_rate)

        individual_genes = self.population[individual]

        for point in mutating_points:
            individual_genes[point] = gauss(individual_genes[point], 1)

    @staticmethod
    def random_range(upper_limit: float, lower_limit: float) -> float:
        return random() * (upper_limit - lower_limit) + lower_limit


def softplus(x: float) -> float:
    return m.log(1 + m.exp(x))


if __name__ == "__main__":

    g = Genetic(10, 5, 5, -5, softplus)
    print(g.population, g._population_fitness(), sep="\n", end="\n\n")
    g.next_generation()
    print(g.population, g._population_fitness(), sep="\n", end="\n\n")
