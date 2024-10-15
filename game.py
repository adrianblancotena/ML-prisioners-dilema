# game.py
from genetic_ai import GeneticAI
from player import AlwaysCooperate, AlwaysDefect, RandomPlayer, TitForTat
import random
def play_round(player1, player2):
    decision1 = player1.decision()
    decision2 = player2.decision()

    if decision1 and decision2:
        player1.coins += 3
        player2.coins += 3
    elif not decision1 and decision2:
        player1.coins += 5
        player2.coins += 0
    elif decision1 and not decision2:
        player1.coins += 0
        player2.coins += 5
    else:  # ambos no cooperan
        player1.coins += 1
        player2.coins += 1

    if isinstance(player1, TitForTat):
        player1.update_decision(decision2)
    if isinstance(player2, TitForTat):
        player2.update_decision(decision1)


def train_ai_for_opponent(opponent, generations=300, population_size=50, mutation_rate=0.1, name="Genetic AI"):
    population = [GeneticAI(name=name) for _ in range(population_size)]

    for generation in range(generations):
        for ai in population:
            ai.reset()
            opponent.reset()
            for _ in range(10):
                play_round(ai, opponent)

        population.sort(key=lambda x: x.coins, reverse=True)
        top_half = population[:population_size // 2]

        new_population = top_half[:]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(top_half, 2)
            child_strategy = parent1.crossover(parent2)
            child_ai = GeneticAI(name=name)
            child_ai.strategy = child_strategy
            child_ai.strategy = child_ai.mutate(mutation_rate)
            new_population.append(child_ai)

        population = new_population

    best_ai = population[0]
    best_ai.save()
    return best_ai
