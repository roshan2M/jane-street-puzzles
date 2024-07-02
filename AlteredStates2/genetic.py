from collections import defaultdict
from typing import Dict, List

from scorer import N, State, computeScore

import random

class GeneticAlgorithm:
    def __init__(self, letterWeights: Dict[str, int]):
        self.choices = "abcdefghijklmnopqrstuvwxyz"
        self.weights = [letterWeights[c] for c in self.choices]

    def fitness(self, input: str) -> int:
        return computeScore(input)

    def selection(self, population: List[str], popFitness: List[int]) -> str:
        idx1 = random.randint(0, len(population)-1)
        idx2 = random.randint(0, len(population)-1)
        bestIdx = max(idx1, idx2, key = lambda i : popFitness[i])
        return population[bestIdx]

    def crossover(self, parent1: str, parent2: str) -> tuple[str, str]:
        # Single-point crossover at a random point
        crossover = random.randint(1, len(parent1) - 2)
        child1 = parent1[:crossover] + parent2[crossover:]
        child2 = parent2[:crossover] + parent1[crossover:]
        return child1, child2

    def mutation(self, chromosome: str, mutation_rate: float) -> str:
        # Flip bits with a probability (mutation_rate)
        mutated_chromosome = list(chromosome)
        for i in range(len(chromosome)):
            if random.random() < mutation_rate:
                mutated_chromosome[i] = random.choices(self.choices, weights=self.weights)[0]
        return "".join(mutated_chromosome)

    def buildChromosome(self, chromosomeLen: int) -> str:
        return "".join(random.choices(self.choices, weights=self.weights, k=chromosomeLen))

    def initialPopulation(self, popSize: int, chromosomeLen: int) -> List[str]:
        return [self.buildChromosome(chromosomeLen) for _ in range(popSize)]

    def solve(self, popSize: int, chromosomeLen: int, generations: int, mutationRate: float) -> tuple[str, int, List[int]]:
        population = self.initialPopulation(popSize, chromosomeLen)

        maxFitnessPerGen = []
        bestChromosome = None
        maxFitness = 0
        for _ in range(generations):
            nextPop = []
            popFitness = [self.fitness(individual) for individual in population]
            for _ in range(int(popSize/2)):
                parents = random.choices(population, weights = popFitness, k = 2)
                child1, child2 = self.crossover(parents[0], parents[1])
                nextPop.append(self.mutation(child1, mutationRate))
                nextPop.append(self.mutation(child2, mutationRate))
            population = nextPop

            bestPopChromosome = max(population, key=self.fitness)
            maxPopFitness = self.fitness(bestPopChromosome)
            maxFitnessPerGen.append(maxPopFitness)
            if maxPopFitness > maxFitness:
                bestChromosome = bestPopChromosome
                maxFitness = maxPopFitness

        return bestChromosome, maxFitness, maxFitnessPerGen

def computeLetterWeights() -> Dict[str, int]:
    # Create map of char -> weight
    weights = defaultdict(float)
    for state in State:
        name = state.value[0]
        for c in state.value[0]:
            weights[c] += float(state.value[1]) / len(name)
    # Normalize weights between 0 and 1
    totalWeights = sum(weights.values())
    for c in weights.keys():
        weights[c] /= totalWeights
    return weights

genetic = GeneticAlgorithm(computeLetterWeights())
bestBoard, maxScore, maxScorePerGen = genetic.solve(50, N*N, 100, 0.005)
print(maxScorePerGen)
print("bestBoard: ", bestBoard, ", maxScore: ", maxScore)

# print(random.choices("abc", weights=[0.2, 0.5, 0.3], k=3))
