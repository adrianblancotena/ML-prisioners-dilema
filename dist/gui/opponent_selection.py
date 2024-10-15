import tkinter as tk
from tkinter import ttk
from game import run_game

class OpponentSelection(tk.Frame):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.main_app = main_app

        self.opponent_label = tk.Label(self, text="Selecciona el oponente", font=("Arial", 14))
        self.opponent_label.pack(pady=10)

        self.opponent_var = tk.StringVar(value="AlwaysCooperate")
        self.opponent_menu = tk.OptionMenu(self, self.opponent_var, "AlwaysCooperate", "AlwaysDefect", "RandomPlayer", "TitForTat")
        self.opponent_menu.pack(pady=10)

        self.test_button = tk.Button(self, text="Probar IA contra oponente", font=("Arial", 14), command=self.test_ai_phase)
        self.test_button.pack(pady=10)

    def test_ai_phase(self):
        selected_opponent = self.opponent_var.get()
        result = run_game(selected_opponent)  # Ejecuta el juego y obtiene el resultado
        self.main_app.result_display.result_label.config(text=result)
