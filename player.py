# player.py
import random


class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.coins = 0

    def decision(self):
        """Método a ser implementado por cada tipo de jugador."""
        pass

    def reset(self):
        """Resetea las monedas al inicio de una nueva ronda."""
        self.coins = 0


class AlwaysCooperate(Player):
    def decision(self):
        return True  # Siempre coopera


class AlwaysDefect(Player):
    def decision(self):
        return False  # Nunca coopera


class RandomPlayer(Player):
    def decision(self):
        return random.choice([True, False])  # Coopera o no de forma aleatoria


class TitForTat(Player):
    def __init__(self):
        super().__init__()
        self.last_opponent_decision = True  # Asume que cooperó en la primera ronda

    def decision(self):
        # Retorna la última decisión del oponente
        return self.last_opponent_decision

    def update(self, opponent_decision):
        # Actualiza la última decisión del oponente
        self.last_opponent_decision = opponent_decision


