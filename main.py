# main.py
import tkinter as tk
from gui import PrisonerDilemmaGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1600x1600")  # Tamaño de la ventana
    root.title("Dilema del Prisionero - Simulador IA")

    # Inicializar la GUI
    app = PrisonerDilemmaGUI(root)

    # Iniciar el bucle de la aplicación
    root.mainloop()
