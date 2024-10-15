#player.py
class Player:

    def __init__(self, name="Player"):
        self.name = name
        self.coins = 0

    def reset(self):
        self.coins = 0


class AlwaysCooperate(Player):
    def decision(self):
        return True  # Siempre coopera

class AlwaysDefect(Player):
    def decision(self):
        return False  # Nunca coopera

class RandomPlayer(Player):
    def decision(self):
        import random
        return random.choice([True, False])  # Elige aleatoriamente

class TitForTat(Player):
    def __init__(self):
        super().__init__()
        self.last_opponent_decision = True  # Asume que cooperó en la primera ronda

    def decision(self):
        # Retorna la última decisión del oponente
        return self.last_opponent_decision

    def update_decision(self, opponent_decision):
        # Actualiza la última decisión del oponente
        self.last_opponent_decision = opponent_decision

