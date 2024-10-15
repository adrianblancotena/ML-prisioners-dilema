# main.py
import tkinter as tk
from gui import PrisonerDilemmaGUI

if __name__ == "__main__":
    root = tk.Tk()


    # Inicializar la GUI
    app = PrisonerDilemmaGUI(root)

    # Iniciar el bucle de la aplicación
    root.mainloop()
