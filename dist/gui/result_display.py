import tkinter as tk

class ResultDisplay(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.result_label = tk.Label(self, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        # Aquí puedes añadir otros widgets para mostrar los resultados
