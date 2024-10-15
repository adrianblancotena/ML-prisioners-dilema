# gui.py
import webbrowser  # Make sure to import the webbrowser library
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
        self.root.title("Prisoner's Dilemma - Trained AI")

        # Adjust the window size
        self.root.geometry("1800x1000")  # Width x Height

        # Set the window to fullscreen mode
        self.root.attributes("-fullscreen", True)  # Activates fullscreen mode

        # Allow exiting fullscreen mode by pressing Escape
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Title
        self.title_label = tk.Label(root, text="Prisoner's Dilemma", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        # Texto explicativo
        self.explanation_label = tk.Label(root,  text="Este juego simula el dilema del prisionero, donde dos jugadores pueden elegir cooperar o no.\n\n"
                                               "El objetivo de esta IA es ganar siempre o al menos empatar; en lugar de buscar la mejor estrategia de cabeza, "
                                               "este programa entrena una IA evolutiva que se encarga de encontrar la mejor estrategia para cada oponente.\n\n"
                                               "El botón 'Borrar Memoria de la IA' eliminará la memoria almacenada para permitir un nuevo entrenamiento.",
                                            wraplength=800, justify="left", font=("Arial", 12))
        self.explanation_label.pack(pady=10)

        self.label = tk.Label(root, text="Select an option", font=("Arial", 14))
        self.label.pack(pady=20)

        # Frame to contain Train and Clear Memory buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.train_button = tk.Button(self.button_frame, text="Train AI", font=("Arial", 14), command=self.train_ai_phase)
        self.train_button.pack(side="left", padx=5)

        self.clear_memory_button = tk.Button(self.button_frame, text="Clear AI Memory", font=("Arial", 14), command=self.clear_ai_memory)
        self.clear_memory_button.pack(side="left", padx=5)

        self.opponent_label = tk.Label(root, text="Select an opponent", font=("Arial", 14))
        self.opponent_label.pack(pady=10)

        self.opponent_var = tk.StringVar(value="Always Cooperate")
        self.opponent_menu = tk.OptionMenu(root, self.opponent_var, "Always Cooperate", "Always Defect", "Random Player", "TitForTat")
        self.opponent_menu.pack(pady=10)

        self.test_button = tk.Button(root, text="Test AI Against Opponent", font=("Arial", 14), command=self.test_ai_phase)
        self.test_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # Create a frame for the canvas and scrollbar
        self.scrollable_frame = tk.Frame(root)
        self.scrollable_frame.pack(pady=10)

        # Create the table
        self.table_canvas = tk.Canvas(self.scrollable_frame, width=1115, height=400)  # Adjust the canvas size
        self.table_canvas.pack(side=tk.LEFT)

        # Create the scrollbar
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.table_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the custom table
        self.table = CustomTable(self.table_canvas, 101, 7, bg="white", width=1115, height=3030)
        self.table_canvas.create_window((0, 0), window=self.table, anchor="nw")

        # Configure the canvas to scroll with the scrollbar
        self.table_canvas.configure(yscrollcommand=self.scrollbar.set)

        # Call the update function for the canvas size
        self.update_canvas_size()

        # Create a frame for the links
        self.link_frame = tk.Frame(root)
        self.link_frame.pack(side=tk.BOTTOM, anchor="se", pady=10)  # Adjust to the bottom right corner

        # Link to LinkedIn
        self.linkedin_label = tk.Label(self.link_frame, text="My LinkedIn", fg="blue", cursor="hand2")
        self.linkedin_label.pack(side=tk.LEFT, padx=10)
        self.linkedin_label.bind("<Button-1>",
                                 lambda e: webbrowser.open_new("https://www.linkedin.com/in/adrianblancotena/"))

        # Link to GitHub
        self.github_label = tk.Label(self.link_frame, text="My GitHub", fg="blue", cursor="hand2")
        self.github_label.pack(side=tk.LEFT, padx=10)
        self.github_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/adrianblancotena"))

        # Link to Veritasium video
        self.veritasium_label = tk.Label(self.link_frame, text="Inspired by Veritasium", fg="blue", cursor="hand2")
        self.veritasium_label.pack(side=tk.LEFT, padx=10)
        self.veritasium_label.bind("<Button-1>",
                                   lambda e: webbrowser.open_new("https://youtu.be/mScpHTIi-kM?si=y4bv_uW_iJIeOKFT"))

    def exit_fullscreen(self, event=None):
        """Exits fullscreen mode."""
        self.root.attributes("-fullscreen", False)

    def update_canvas_size(self):
        """Updates the canvas size based on the total size of the table."""
        self.table.update_idletasks()  # Ensure the canvas has been fully rendered
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def clear_ai_memory(self):
        """Deletes the AI's JSON file if it exists."""
        json_file = 'saved_strategies.json'  # Change this path to the correct file
        try:
            if os.path.exists(json_file):
                os.remove(json_file)
                self.result_label.config(text="AI memory cleared.")
            else:
                self.result_label.config(text="Memory has already been cleared.")
        except Exception as e:
            self.result_label.config(text=f"Error clearing the file: {e}")

    def train_ai_phase(self):
        self.result_label.config(text="Training AI against all opponents... (THIS MAY TAKE A FEW SECONDS, PLEASE WAIT) ")
        self.root.update()

        # Train the AI against all opponents
        train_ai_for_opponent(AlwaysCooperate(), name="Against_Cooperate")
        train_ai_for_opponent(AlwaysDefect(), name="Against_Defect")
        train_ai_for_opponent(RandomPlayer(), name="Against_Random")
        train_ai_for_opponent(TitForTat(), name="Against_TitForTat")

        self.result_label.config(text="Training completed. Ready to test!")

    def test_ai_phase(self):
        selected_opponent = self.opponent_var.get()

        # Create the opponent based on the selection
        if selected_opponent == "Always Cooperate":
            opponent = AlwaysCooperate()
            ai = GeneticAI(name="Against_Cooperate")
        elif selected_opponent == "Always Defect":
            opponent = AlwaysDefect()
            ai = GeneticAI(name="Against_Defect")
        elif selected_opponent == "Random Player":
            opponent = RandomPlayer()
            ai = GeneticAI(name="Against_Random")
        elif selected_opponent == "TitForTat":
            opponent = TitForTat()
            ai = GeneticAI(name="Against_TitForTat")

        # Clear the table before starting
        self.table.delete("all")  # This will delete all cells, including headers
        self.table.create_column_headers()  # Add the headers back

        ai.reset()
        opponent.reset()
        total_ai_coins = 0  # Initialize AI total coins
        total_opponent_coins = 0  # Initialize opponent total coins

        # Store the results in a temporary list
        results = []

        for round_number in range(1, 101):
            # Hacer que ambos jugadores tomen decisiones
            ai_decision = ai.decision()  # Toma la decisión de la IA
            opponent_decision = opponent.decision()  # Toma la decisión del oponente

            # Update the opponent's decision (TitForTat) with the AI's decision
            if isinstance(opponent, TitForTat):
                opponent.update_decision(ai_decision)

            # Calculate coins won in this round
            if ai_decision and opponent_decision:
                ai_coins = 3
                opponent_coins = 3
            elif ai_decision and not opponent_decision:
                ai_coins = 0
                opponent_coins = 5
            elif not ai_decision and opponent_decision:
                ai_coins = 5
                opponent_coins = 0
            else:
                ai_coins = 1
                opponent_coins = 1

            # Update total coins
            total_ai_coins += ai_coins
            total_opponent_coins += opponent_coins

            # Store the round result
            results.append((round_number, ai_decision, opponent_decision, total_ai_coins, total_opponent_coins))

        # Actualiza la decisión final de TitForTat después de la última ronda
        if isinstance(opponent, TitForTat):
            opponent.update_decision(ai_decision)  # Actualiza la decisión con la última decisión de IA

        # Display final results
        final_result = f"Final Results:\nAI total coins: {total_ai_coins}\nOpponent total coins: {total_opponent_coins}"
        self.result_label.config(text=final_result)


if __name__ == "__main__":
    root = tk.Tk()
    app = PrisonerDilemmaGUI(root)
    root.mainloop()
