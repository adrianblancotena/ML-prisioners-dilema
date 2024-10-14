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
        self.last_opponent_move = True  # Empieza cooperando

    def decision(self):
        return self.last_opponent_move  # Coopera si el oponente cooperó en la última ronda

    def update(self, opponent_move):
        self.last_opponent_move = opponent_move
