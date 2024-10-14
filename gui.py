import tkinter as tk
from tkinter import ttk
from game import train_ai_for_opponent, play_round
from player import AlwaysCooperate, AlwaysDefect, RandomPlayer, TitForTat
from genetic_ai import GeneticAI

class PrisonerDilemmaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dilema del Prisionero - IA Entrenada")

        self.label = tk.Label(root, text="Selecciona una opción", font=("Arial", 14))
        self.label.pack(pady=20)

        self.train_button = tk.Button(root, text="Entrenar IA", font=("Arial", 14), command=self.train_ai_phase)
        self.train_button.pack(pady=10)

        self.opponent_label = tk.Label(root, text="Selecciona el oponente", font=("Arial", 14))
        self.opponent_label.pack(pady=10)

        self.opponent_var = tk.StringVar(value="AlwaysCooperate")
        self.opponent_menu = tk.OptionMenu(root, self.opponent_var, "AlwaysCooperate", "AlwaysDefect", "RandomPlayer", "TitForTat")
        self.opponent_menu.pack(pady=10)

        self.test_button = tk.Button(root, text="Probar IA contra oponente", font=("Arial", 14), command=self.test_ai_phase)
        self.test_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # Frame para contener el Treeview y el Scrollbar
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Scrollbar vertical
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        # Tabla para mostrar las acciones de cada ronda
        self.tree = ttk.Treeview(self.frame, columns=("Ronda", "Acción IA", "Monedas IA", "Acción Oponente", "Monedas Oponente"), show="headings", height=15, yscrollcommand=self.scrollbar.set)
        self.tree.heading("Ronda", text="Ronda")
        self.tree.heading("Acción IA", text="Acción IA")
        self.tree.heading("Monedas IA", text="Monedas IA")
        self.tree.heading("Acción Oponente", text="Acción Oponente")
        self.tree.heading("Monedas Oponente", text="Monedas Oponente")
        self.tree.pack(side="left")

        # Configurar el scrollbar para que funcione con la tabla
        self.scrollbar.config(command=self.tree.yview)

    def train_ai_phase(self):
        self.result_label.config(text="Entrenando IA contra todos los oponentes...")
        self.root.update()

        train_ai_for_opponent(AlwaysCooperate(), name="Against_Cooperate")
        train_ai_for_opponent(AlwaysDefect(), name="Against_Defect")
        train_ai_for_opponent(RandomPlayer(), name="Against_Random")
        train_ai_for_opponent(TitForTat(), name="Against_TitForTat")

        self.result_label.config(text="Entrenamiento completado. ¡Listo para probar!")

    def test_ai_phase(self):
        selected_opponent = self.opponent_var.get()

        if selected_opponent == "AlwaysCooperate":
            opponent = AlwaysCooperate()
            ai = GeneticAI(name="Against_Cooperate")
        elif selected_opponent == "AlwaysDefect":
            opponent = AlwaysDefect()
            ai = GeneticAI(name="Against_Defect")
        elif selected_opponent == "RandomPlayer":
            opponent = RandomPlayer()
            ai = GeneticAI(name="Against_Random")
        elif selected_opponent == "TitForTat":
            opponent = TitForTat()
            ai = GeneticAI(name="Against_TitForTat")

        for row in self.tree.get_children():
            self.tree.delete(row)

        ai.reset()
        opponent.reset()
        for round_number in range(1, 101):
            play_round(ai, opponent)

            decision_ai = "Cooperar" if ai.decision() else "No cooperar"
            decision_opponent = "Cooperar" if opponent.decision() else "No cooperar"

            item_id = self.tree.insert("", "end", values=(round_number, decision_ai, ai.coins, decision_opponent, opponent.coins))

            self.color_row(item_id, ai.decision(), ai.coins, opponent.decision(), opponent.coins)

        result = f"IA ganó con {ai.coins} monedas. Oponente: {opponent.coins} monedas."
        self.result_label.config(text=result)

    def color_row(self, item_id, ai_decision, ai_coins, opponent_decision, opponent_coins):
        # Configuración de colores para las acciones y monedas
        ai_color = "lightgreen" if ai_decision else "lightcoral"
        opponent_color = "lightgreen" if opponent_decision else "lightcoral"
        ai_coins_color = "lightyellow" if ai_coins > 0 else "lightgray"
        opponent_coins_color = "lightyellow" if opponent_coins > 0 else "lightgray"

        # Aplicar los colores individualmente a cada celda en la fila
        self.tree.tag_configure(f"row_{item_id}_ai", background=ai_color)
        self.tree.tag_configure(f"row_{item_id}_opponent", background=opponent_color)
        self.tree.tag_configure(f"row_{item_id}_ai_coins", background=ai_coins_color)
        self.tree.tag_configure(f"row_{item_id}_opponent_coins", background=opponent_coins_color)

        # Asignar las etiquetas a las celdas correspondientes
        self.tree.item(item_id, tags=(f"row_{item_id}_ai", f"row_{item_id}_opponent", f"row_{item_id}_ai_coins", f"row_{item_id}_opponent_coins"))

if __name__ == "__main__":
    root = tk.Tk()
    app = PrisonerDilemmaGUI(root)
    root.mainloop()
