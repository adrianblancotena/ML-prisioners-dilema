#custom_table.py

import tkinter as tk



class CustomTable(tk.Canvas):
    def __init__(self, master, rows, columns, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.rows = rows
        self.columns = columns
        self.cell_width = 160
        self.cell_height = 30
        self.data = [[0 for _ in range(columns)] for _ in range(rows)]
        self.create_table()
        self.create_column_headers()  # Llamar a crear cabeceras

    def create_table(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.draw_cell(row, column, str(self.data[row][column]), "white")

    def draw_cell(self, row, column, value, color):
        x0 = column * self.cell_width
        y0 = row * self.cell_height
        x1 = x0 + self.cell_width
        y1 = y0 + self.cell_height
        self.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
        self.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=value)

    def update_cell(self, row, column, value, color):
        self.draw_cell(row, column, value, color)

    def create_column_headers(self):
        headers = ["Ronda", "Decisión IA", "Monedas IA","Monedas esta ronda" ,"Decisión Oponente", "Monedas esta ronda","Monedas Oponente"]
        for index, header in enumerate(headers):
            self.draw_cell(0, index, header, "lightblue")  # Dibuja en la primera fila
    def update_canvas_size(self):
        """Ajusta el tamaño del lienzo según el contenido de la tabla."""
        # Asegurarse de que la tabla tenga el tamaño correcto
        total_width = sum(cell.winfo_width() for cell in self.cells.values()) // self.columns
        total_height = sum(cell.winfo_height() for cell in self.cells.values()) // self.rows
        self.config(width=total_width, height=total_height)