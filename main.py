import random

import matplotlib.pyplot as plt


class Organism:
    def __init__(self, min_n2_conc, max_co2_conc, mutation_prob):
        self.min_n2 = min_n2_conc
        self.max_co2 = max_co2_conc
        self.mutation_prob = mutation_prob

    def breed(self, current_n2, current_co2):
        n2_const = current_n2 - self.min_n2
        co2_const = (self.max_co2 - current_co2) / self.max_co2

        if n2_const < 0 or co2_const < 0:
            return None

        reproduction_prob = n2_const * co2_const
        if not random.random() < reproduction_prob:
            return None

        new_min_n2 = self.min_n2
        new_max_co2 = self.max_co2
        new_mutation_prob = self.mutation_prob
        if random.random() < self.mutation_prob:
            if self.min_n2 - 0.1 >= 0:
                new_min_n2 -= 0.1
            if self.max_co2 + 0.1 <= 1:
                new_max_co2 += 0.1
            new_mutation_prob = 1 - self.mutation_prob

        return Organism(new_min_n2, new_max_co2, new_mutation_prob)


class Population:
    def __init__(self, min_n2_conc, max_co2_conc, mutation_prob, size):
        self.population = list()

        self.generate_population(min_n2_conc, max_co2_conc, mutation_prob, size)

    def generate_population(self, min_n2_conc, max_co2_conc, mutation_prob, size):
        for _ in range(size):
            self.population.append(Organism(min_n2_conc, max_co2_conc, mutation_prob))

    def step(self, current_n2, current_co2):
        for organism in self.population:
            new_organism = organism.breed(current_n2, current_co2)
            if new_organism:
                self.population.append(new_organism)

    def get_size(self):
        return len(self.population)


class Environment:
    def __init__(self, n2_conc, co2_conc):
        self.current_n2 = n2_conc
        self.current_co2 = co2_conc

        self.population = None

    def introduce_population(self, pop_size, mutation):
        self.population = Population(
            self.current_n2, self.current_co2, mutation, pop_size
        )

    def increase_n2(self, increase):
        if increase < 0 or self.current_n2 + self.current_co2 + increase > 1:
            raise ValueError
        self.current_n2 += increase

    def increase_co2(self, increase):
        if increase < 0 or self.current_n2 + self.current_co2 + increase > 1:
            raise ValueError
        self.current_co2 += increase

    def decrease_n2(self, decrease):
        if decrease < 0 or self.current_n2 - decrease < 0:
            raise ValueError
        self.current_n2 -= decrease

    def decrease_co2(self, decrease):
        if decrease < 0 or self.current_co2 - decrease < 0:
            raise ValueError
        self.current_co2 -= decrease

    def time_step(self):
        if not self.population:
            raise ValueError
        self.population.step(self.current_n2, self.current_co2)

    def get_pop_size(self):
        return self.population.get_size()


def simulate_breeding(
    length, start_pop, mutation, start_n2, start_co2, change_frequency
):
    env = Environment(start_n2, start_co2)
    env.introduce_population(start_pop, mutation)
    pop_size = []
    for i in range(length):
        env.time_step()
        pop_size.append(env.get_pop_size())
        if i % change_frequency == 0:
            env.increase_n2(0.01)
            env.decrease_co2(0.01)

    return pop_size


def main():
    pop_size = simulate_breeding(100, 10, 0.5, 0.2, 0.5, 5)
    plt.plot(pop_size)
    plt.xlabel("time passed")
    plt.ylabel("population size")
    plt.suptitle("Change of population size")
    plt.show()


# Ak dusík stúpa a oxid uhličitý klesá, veľkosť populácie sa zvyšuje
# Ak sa zmení naopak alebo sa zmení iba jeden plyn, veľkosť populácie sa nezmení


if __name__ == "__main__":
    main()
