import tkinter as tk
from player import AlwaysCooperate, AlwaysDefect, RandomPlayer, TitForTat
from game import train_ai_for_opponent

class TrainingFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.result_label = tk.Label(self, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.train_button = tk.Button(self, text="Entrenar IA", font=("Arial", 14), command=self.train_ai_phase)
        self.train_button.pack(side="left", padx=5)

        self.clear_memory_button = tk.Button(self, text="Borrar Memoria de la IA", font=("Arial", 14), command=self.clear_ai_memory)
        self.clear_memory_button.pack(side="left", padx=5)

    def clear_ai_memory(self):
        # Aquí puedes implementar la lógica para borrar la memoria de la IA
        pass

    def train_ai_phase(self):
        self.result_label.config(text="Entrenando IA contra todos los oponentes...")
        self.master.update()

        # Entrenamiento de la IA contra todos los oponentes
        train_ai_for_opponent(AlwaysCooperate(), name="Against_Cooperate")
        train_ai_for_opponent(AlwaysDefect(), name="Against_Defect")
        train_ai_for_opponent(RandomPlayer(), name="Against_Random")
        train_ai_for_opponent(TitForTat(), name="Against_TitForTat")

        self.result_label.config(text="Entrenamiento completado. ¡Listo para probar!")
