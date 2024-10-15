# gui.py

import tkinter as tk
from tkinter import ttk
import os
from game import train_ai_for_opponent, play_round
from player import AlwaysCooperate, AlwaysDefect, RandomPlayer, TitForTat
from genetic_ai import GeneticAI
from custom_table import CustomTable

class PrisonerDilemmaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dilema del Prisionero - IA Entrenada")


        # Ajustar el tamaño de la ventana
        self.root.geometry("1920x1080")  # Ancho x Alto

        self.root.configure(bg="#2E2E2E")  # Color gris oscuro PARA LA NOCHE
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

        # Crear la tabla
        self.table_canvas = tk.Canvas(self.scrollable_frame, width=1115, height=400)  # Cambiar el tamaño del lienzo
        self.table_canvas.pack(side=tk.LEFT)

        # Crear la barra de desplazamiento
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.table_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Crear la tabla personalizada
        self.table = CustomTable(self.table_canvas, 101, 7, bg="white", width=1115, height=3030)
        self.table_canvas.create_window((0, 0), window=self.table, anchor="nw")

        # Configurar el lienzo para que se desplace con la barra
        self.table_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Llamar a la función de actualización para el tamaño del lienzo
        self.update_canvas_size()



    def update_canvas_size(self):
        """Actualiza el tamaño del lienzo según el tamaño total de la tabla."""
        self.table.update_idletasks()  # Asegura que el lienzo haya sido completamente renderizado
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

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
        self.table.create_column_headers()  # Añade de nuevo las cabeceras

        ai.reset()
        opponent.reset()
        total_ai_coins = 0  # Inicializa el total de monedas IA
        total_opponent_coins = 0  # Inicializa el total de monedas del oponente

        # Almacena los resultados en una lista temporal
        results = []

        for round_number in range(1, 101):
            play_round(ai, opponent)

            decision_ai = ai.decision()
            decision_opponent = opponent.decision()

            # Actualiza la decisión del oponente (TitForTat) con la decisión de la IA
            if isinstance(opponent, TitForTat):
                opponent.update_decision(decision_ai)

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

            # Sumar las monedas a los totales
            total_ai_coins += ai_coins
            total_opponent_coins += opponent_coins

            # Almacenar los resultados en la lista
            results.append((round_number, decision_ai, ai_coins, total_ai_coins, decision_opponent, opponent_coins,
                            total_opponent_coins))

            # Puedes actualizar la tabla cada 10 rondas, por ejemplo
            if round_number % 10 == 0:
                for r in results:
                    self.table.update_cell(r[0], 0, r[0], "white")  # Ronda
                    self.table.update_cell(r[0], 1, "Cooperar" if r[1] else "No cooperar",
                                           "lightgreen" if r[1] else "lightcoral")  # Decisión IA
                    self.table.update_cell(r[0], 2, r[2], "lightyellow" if r[2] > 0 else "lightgray")  # Monedas IA
                    self.table.update_cell(r[0], 3, r[3], "lightyellow")  # Total Monedas IA
                    self.table.update_cell(r[0], 4, "Cooperar" if r[4] else "No cooperar",
                                           "lightgreen" if r[4] else "lightcoral")  # Decisión Oponente
                    self.table.update_cell(r[0], 5, r[5],
                                           "lightyellow" if r[5] > 0 else "lightgray")  # Monedas Oponente
                    self.table.update_cell(r[0], 6, r[6], "lightyellow")  # Total Oponente
                results.clear()  # Limpiar la lista de resultados


        # Actualizar el resultado total en la parte inferior
        self.result_label.config(
            text=f"Resultados: IA total de monedas: {total_ai_coins}, Oponente total de monedas: {total_opponent_coins}")



