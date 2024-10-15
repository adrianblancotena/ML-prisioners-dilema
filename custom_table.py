import tkinter as tk
from tkinter import ttk

class CustomTable(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = ttk.Treeview(self)
        self.tree.pack(expand=True, fill='both')

        self.tree["columns"] = ("Round", "Player Decision", "Opponent Decision", "Coins")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

    def add_row(self, round_num, player_decision, opponent_decision, coins):
        self.tree.insert("", "end", values=(round_num, player_decision, opponent_decision, coins))
