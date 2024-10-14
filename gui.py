#gui.py
import tkinter as tk
from tkinter import ttk
import os
from game import train_ai_for_opponent, play_round
from player import AlwaysCooperate, AlwaysDefect, RandomPlayer, TitForTat
from genetic_ai import GeneticAI
from custom_table import CustomTable  # Importa la clase desde el nuevo archivo

class PrisonerDilemmaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dilema del Prisionero - IA Entrenada")

        # Ajustar el tamaño de la ventana
        self.root.geometry("1920x1080")  # Ancho x Alto

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
        self.train_button.pack(side="left", padx=5)

        self.clear_memory_button = tk.Button(self.button_frame, text="Borrar Memoria de la IA", font=("Arial", 14), command=self.clear_ai_memory)
        self.clear_memory_button.pack(side="left", padx=5)

        self.opponent_label = tk.Label(root, text="Selecciona el oponente", font=("Arial", 14))
        self.opponent_label.pack(pady=10)

        self.opponent_var = tk.StringVar(value="AlwaysCooperate")
        self.opponent_menu = tk.OptionMenu(root, self.opponent_var, "AlwaysCooperate", "AlwaysDefect", "RandomPlayer", "TitForTat")
        self.opponent_menu.pack(pady=10)

        self.test_button = tk.Button(root, text="Probar IA contra oponente", font=("Arial", 14), command=self.test_ai_phase)
        self.test_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # Crear el marco para el lienzo y la barra de desplazamiento
        self.scrollable_frame = tk.Frame(root)
        self.scrollable_frame.pack(pady=10)

        # Crear el lienzo
        self.table_canvas = tk.Canvas(self.scrollable_frame, width=800)
        self.table_canvas.pack(side=tk.LEFT)

        # Crear la barra de desplazamiento
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.table_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Crear la tabla personalizada
        self.table = CustomTable(self.table_canvas, 100, 5, bg="white", width=800,
                                 height=3030)  # Ajusta el ancho y alto del lienzo  #3030 porque son 101 filas de 30 px
        self.table_canvas.create_window((0, 0), window=self.table, anchor="nw")

        # Configurar el lienzo para que se desplace con la barra
        self.table_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Llamar a la función de actualización para el tamaño del lienzo
        self.table.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))

        # Nombres de las columnas
        self.create_column_headers()

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

        # Entrenamiento de la IA contra todos los oponentes
        train_ai_for_opponent(AlwaysCooperate(), name="Against_Cooperate")
        train_ai_for_opponent(AlwaysDefect(), name="Against_Defect")
        train_ai_for_opponent(RandomPlayer(), name="Against_Random")
        train_ai_for_opponent(TitForTat(), name="Against_TitForTat")

        self.result_label.config(text="Entrenamiento completado. ¡Listo para probar!")

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

        # Limpiar la tabla antes de empezar
        self.table.delete("all")  # Esto eliminará todas las celdas, incluidas las cabeceras

        # Vuelve a dibujar las cabeceras después de limpiar
        self.create_column_headers()  # Esto es necesario para que las cabeceras se mantengan

        ai.reset()
        opponent.reset()
        for round_number in range(1, 101):
            play_round(ai, opponent)

            # Obtener las decisiones de la IA y del oponente
            decision_ai = ai.decision()
            decision_opponent = opponent.decision()

            # Calcular las monedas ganadas en esta ronda
            if decision_ai and decision_opponent:
                ai_coins = 3
                opponent_coins = 3
            elif decision_ai and not decision_opponent:
                ai_coins = 0
                opponent_coins = 5
            elif not decision_ai and decision_opponent:
                ai_coins = 5
                opponent_coins = 0
            else:  # ambos no cooperan
                ai_coins = 1
                opponent_coins = 1

            # Actualizar la tabla con los resultados de la ronda
            self.table.update_cell(round_number, 0, round_number,
                                   "white")  # Usar round_number aquí en lugar de round_number - 1
            self.table.update_cell(round_number, 1, "Cooperar" if decision_ai else "No cooperar",
                                   "lightgreen" if decision_ai else "lightcoral")
            self.table.update_cell(round_number, 2, ai_coins, "lightyellow" if ai_coins > 0 else "lightgray")
            self.table.update_cell(round_number, 3, "Cooperar" if decision_opponent else "No cooperar",
                                   "lightgreen" if decision_opponent else "lightcoral")
            self.table.update_cell(round_number, 4, opponent_coins,
                                   "lightyellow" if opponent_coins > 0 else "lightgray")

        result = f"IA ganó con {ai.coins} monedas. Oponente: {opponent.coins} monedas."
        self.result_label.config(text=result)




    def create_column_headers(self):
        """Crea los encabezados de las columnas en la tabla."""
        headers = ["Ronda", "Decisión IA", "Monedas IA", "Decisión Oponente", "Monedas Oponente"]
        for index, header in enumerate(headers):
            self.table.update_cell(0, index, header, "lightblue")  # Dibuja en la primera fila




if __name__ == "__main__":
    root = tk.Tk()
    app = PrisonerDilemmaGUI(root)
    root.mainloop()
