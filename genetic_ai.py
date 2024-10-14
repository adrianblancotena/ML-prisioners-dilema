# genetic_ai.py
import random
from player import Player
from save_progress import save_strategy, load_strategy

class GeneticAI(Player):
    def __init__(self, name="Genetic AI", strategy_length=10):
        super().__init__(name=name)
        # Carga la estrategia guardada si existe, si no crea una nueva
        saved_strategy = load_strategy(name)
        if saved_strategy:
            self.strategy = saved_strategy
        else:
            self.strategy = [random.choice([True, False]) for _ in range(strategy_length)]
        self.current_round = 0

    def decision(self):
        decision = self.strategy[self.current_round % len(self.strategy)]
        self.current_round += 1
        return decision

    def mutate(self, mutation_rate=0.1):
        new_strategy = self.strategy[:]
        for i in range(len(new_strategy)):
            if random.random() < mutation_rate:
                new_strategy[i] = not new_strategy[i]
        return new_strategy

    def crossover(self, other_ai):
        crossover_point = random.randint(0, len(self.strategy) - 1)
        new_strategy = self.strategy[:crossover_point] + other_ai.strategy[crossover_point:]
        return new_strategy

    def save(self):
        """Guarda la estrategia actual de la IA."""
        save_strategy(self.name, self.strategy)
