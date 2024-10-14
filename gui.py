import tkinter as tk
from tkinter import ttk
import os
from game import train_ai_for_opponent, play_round
from player import AlwaysCooperate, AlwaysDefect, RandomPlayer, TitForTat
from genetic_ai import GeneticAI

class PrisonerDilemmaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dilema del Prisionero - IA Entrenada")

        # Título
        self.title_label = tk.Label(root, text="Dilema del Prisionero", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        # Texto explicativo
        self.explanation_label = tk.Label(root, text="Este juego simula el dilema del prisionero, donde dos jugadores pueden elegir cooperar o no. "
                                                      "Al entrenar a la IA, se optimiza su estrategia contra diferentes oponentes. "
                                                      "El botón 'Borrar Memoria de la IA' eliminará la memoria almacenada para permitir un nuevo entrenamiento.",
                                            wraplength=600, justify="left", font=("Arial", 12))
        self.explanation_label.pack(pady=10)

        self.label = tk.Label(root, text="Selecciona una opción", font=("Arial", 14))
        self.label.pack(pady=20)

        # Frame para contener los botones de Entrenar y Borrar Memoria
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.train_button = tk.Button(self.button_frame, text="Entrenar IA", font=("Arial", 14), command=self.train_ai_phase)
        self.train_button.pack(side="left", padx=5)  # Añadido un margen a la derecha

        self.clear_memory_button = tk.Button(self.button_frame, text="Borrar Memoria de la IA", font=("Arial", 14), command=self.clear_ai_memory)
        self.clear_memory_button.pack(side="left", padx=5)  # Añadido un margen a la izquierda

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

    def clear_ai_memory(self):
        """Borra el archivo JSON de la IA si existe."""
        json_file = 'saved_strategies.json'  # Cambia esta ruta al archivo correcto
        try:
            if os.path.exists(json_file):
                os.remove(json_file)
                self.result_label.config(text="Memoria de la IA borrada.")
            else:
                self.result_label.config(text="La memoria ya ha sido borrada.")
        except Exception as e:
            self.result_label.config(text=f"Error al borrar el archivo: {e}")

    def train_ai_phase(self):
        self.result_label.config(text="Entrenando IA contra todos los oponentes...")
        self.root.update()

        train_ai_for_opponent(AlwaysCooperate(), name="Against_Cooperate")
        train_ai_for_opponent(AlwaysDefect(), name="Against_Defect")
        train_ai_for_opponent(RandomPlayer(), name="Against_Random")
        train_ai_for_opponent(TitForTat(), name="Against_TitForTat")

        self.result_label.config(text="Entrenamiento completado. ¡Listo para probar!")

    def color_row(self, item_id, ai_decision, ai_coins, opponent_decision, opponent_coins):
        # Colores según las decisiones
        ai_action_color = "lightgreen" if ai_decision else "lightcoral"
        opponent_action_color = "lightgreen" if opponent_decision else "lightcoral"

        # Colores para monedas
        ai_coins_color = "lightyellow" if ai_coins > 0 else "lightgray"
        opponent_coins_color = "lightyellow" if opponent_coins > 0 else "lightgray"

        # Aplicar colores a las celdas de acción
        self.tree.item(item_id, values=(
            self.tree.item(item_id)['values'][0],  # Ronda
            "Cooperar" if ai_decision else "No cooperar",  # Acción IA
            ai_coins,  # Monedas IA
            "Cooperar" if opponent_decision else "No cooperar",  # Acción Oponente
            opponent_coins  # Monedas Oponente
        ))

        # Configuración de tags para aplicar colores
        self.tree.tag_configure(f"ai_action_{item_id}", background=ai_action_color)
        self.tree.tag_configure(f"opponent_action_{item_id}", background=opponent_action_color)
        self.tree.tag_configure(f"ai_coins_{item_id}", background=ai_coins_color)
        self.tree.tag_configure(f"opponent_coins_{item_id}", background=opponent_coins_color)

        # Asignar tags a las celdas correspondientes
        self.tree.item(item_id, tags=(
        f"ai_action_{item_id}", f"opponent_action_{item_id}", f"ai_coins_{item_id}", f"opponent_coins_{item_id}"))

        # Configurar el color específico para cada celda después de insertar
        self.tree.item(item_id, tags=("row",))

    def test_ai_phase(self):
        selected_opponent = self.opponent_var.get()

        # Crear el oponente según la selección
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

        # Limpiar el Treeview antes de empezar
        for row in self.tree.get_children():
            self.tree.delete(row)

        ai.reset()
        opponent.reset()
        for round_number in range(1, 101):
            play_round(ai, opponent)

            # Aquí obtenemos las decisiones de la IA y del oponente
            decision_ai = ai.decision()  # Esta llamada debería ser después de `play_round`
            decision_opponent = opponent.decision()  # Esto está bien

            # Definir el texto basado en las decisiones
            decision_text_ai = "Cooperar" if decision_ai else "No cooperar"
            decision_text_opponent = "Cooperar" if decision_opponent else "No cooperar"

            item_id = self.tree.insert("", "end",
                                       values=(round_number, decision_ai, ai.coins, decision_opponent, opponent.coins))
            self.color_row(item_id, ai.decision(), ai.coins, opponent.decision(), opponent.coins)

        result = f"IA ganó con {ai.coins} monedas. Oponente: {opponent.coins} monedas."
        self.result_label.config(text=result)


if __name__ == "__main__":
    root = tk.Tk()
    app = PrisonerDilemmaGUI(root)
    root.mainloop()
