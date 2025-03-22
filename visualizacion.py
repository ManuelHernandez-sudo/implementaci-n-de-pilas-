import tkinter as tk
from tkinter import ttk
import random

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Algoritmos de Ordenamiento")
        
        self.array = []
        self.bars = []
        self.is_sorting = False  # Para evitar múltiples ejecuciones

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        control_frame = ttk.Frame(root)
        control_frame.pack()

        self.generate_button = ttk.Button(control_frame, text="Generar Lista Aleatoria", command=self.generate_array)
        self.generate_button.grid(row=0, column=0, padx=5, pady=5)

        self.bubble_sort_button = ttk.Button(control_frame, text="Bubble Sort", command=lambda: self.bubble_sort(0, 0))
        self.bubble_sort_button.grid(row=0, column=1, padx=5, pady=5)

        self.selection_sort_button = ttk.Button(control_frame, text="Selection Sort", command=lambda: self.selection_sort(0, 0))
        self.selection_sort_button.grid(row=0, column=2, padx=5, pady=5)

        self.reset_button = ttk.Button(control_frame, text="Reiniciar", command=self.reset)
        self.reset_button.grid(row=0, column=3, padx=5, pady=5)

        self.speed_scale = ttk.Scale(control_frame, from_=10, to=500, orient="horizontal")
        self.speed_scale.set(100)
        self.speed_scale.grid(row=0, column=4, padx=5, pady=5)

    def generate_array(self):
        if self.is_sorting:
            return
        self.array = [random.randint(10, 300) for _ in range(20)]
        self.draw_bars()

    def draw_bars(self):
        self.canvas.delete("all")
        self.bars = []
        bar_width = 600 / len(self.array)
        for i, value in enumerate(self.array):
            x0 = i * bar_width
            y0 = 400 - value
            x1 = (i + 1) * bar_width
            y1 = 400
            bar = self.canvas.create_rectangle(x0, y0, x1, y1, fill='blue')
            self.bars.append(bar)

    def update_bar(self, index, value, color='blue'):
        bar_width = 600 / len(self.array)
        x0 = index * bar_width
        y0 = 400 - value
        x1 = (index + 1) * bar_width
        self.canvas.coords(self.bars[index], x0, y0, x1, 400)
        self.canvas.itemconfig(self.bars[index], fill=color)

    def disable_buttons(self, state):
        self.generate_button.config(state=state)
        self.bubble_sort_button.config(state=state)
        self.selection_sort_button.config(state=state)
        self.reset_button.config(state=state)

    def bubble_sort(self, i, j):
        if i >= len(self.array) - 1:
            self.is_sorting = False
            self.disable_buttons("normal")
            return
        
        if j < len(self.array) - 1 - i:
            if self.array[j] > self.array[j + 1]:
                self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                self.update_bar(j, self.array[j], 'red')
                self.update_bar(j + 1, self.array[j + 1], 'red')

            self.root.after(int(self.speed_scale.get()), self.bubble_sort, i, j + 1)
        else:
            self.update_bar(len(self.array) - 1 - i, self.array[len(self.array) - 1 - i], 'green')
            self.root.after(int(self.speed_scale.get()), self.bubble_sort, i + 1, 0)

    def selection_sort(self, i, min_idx):
        if i >= len(self.array) - 1:
            self.is_sorting = False
            self.disable_buttons("normal")
            return

        j = i + 1
        while j < len(self.array):
            if self.array[j] < self.array[min_idx]:
                min_idx = j
            j += 1

        self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
        self.update_bar(i, self.array[i], 'red')
        self.update_bar(min_idx, self.array[min_idx], 'red')

        self.root.after(int(self.speed_scale.get()), self.selection_sort, i + 1, i + 1)

    def reset(self):
        if self.is_sorting:
            return
        self.array = []
        self.bars = []
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()