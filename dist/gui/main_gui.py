import tkinter as tk
from training_frame import TrainingFrame
from opponent_selection import OpponentSelection
from result_display import ResultDisplay

class PrisonerDilemmaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dilema del Prisionero - IA Entrenada")
        self.root.geometry("1920x1080")
        self.root.configure(bg="#2E2E2E")

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Dilema del Prisionero", font=("Arial", 20, "bold"), bg="#2E2E2E", fg="white")
        self.title_label.pack(pady=10)

        self.training_frame = TrainingFrame(self.root)
        self.training_frame.pack(pady=10)

        self.opponent_selection = OpponentSelection(self.root, self)
        self.opponent_selection.pack(pady=10)

        self.result_display = ResultDisplay(self.root)
        self.result_display.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PrisonerDilemmaGUI(root)
    root.mainloop()
