import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
from collections import deque

# ---------------- Clase del Grafo ----------------
class Graph:
    def __init__(self):
        self.adj_list = {
            "Yoel": ["Emilio", "Fernando"],
            "Emilio": ["Julia", "Juana", "Pedro"],
            "Fernando": ["Pedro"],
            "Julia": [],
            "Juana": [],
            "Pedro": []
        }

    def add_friendship(self, u1, u2):
        if u1 in self.adj_list and u2 in self.adj_list:
            if u2 not in self.adj_list[u1]:
                self.adj_list[u1].append(u2)
            if u1 not in self.adj_list[u2]:
                self.adj_list[u2].append(u1)

    def get_friends(self, user):
        return self.adj_list.get(user, [])

    def suggest_friends_bfs(self, user):
        if user not in self.adj_list:
            return []
        direct_friends = set(self.adj_list[user])
        suggestions = set()
        visited = set()
        queue = deque([(user, 0)])

        while queue:
            current, level = queue.popleft()
            if level > 2:
                continue
            visited.add(current)
            for neighbor in self.adj_list.get(current, []):
                if neighbor not in visited:
                    queue.append((neighbor, level + 1))
                    if level == 1 and neighbor not in direct_friends and neighbor != user:
                        suggestions.add(neighbor)
                    visited.add(neighbor)
        return list(suggestions)

    def bfs(self, start):
        visited = set()
        queue = deque([start])
        result = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                result.append(node)
                visited.add(node)
                queue.extend(self.adj_list.get(node, []))
        return result

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        result = [start]
        for neighbor in self.adj_list.get(start, []):
            if neighbor not in visited:
                result.extend(self.dfs(neighbor, visited))
        return result

# ---------------- Interfaz Tkinter ----------------
class SocialGraphApp:
    def __init__(self, root):
        self.graph = Graph()
        self.root = root
        self.root.title("Red Social con Grafos")
        self.user_positions = {}

        self.canvas = tk.Canvas(root, bg="white", width=600, height=600)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.setup_ui()
        self.generate_all_positions()
        self.draw_graph()

    def setup_ui(self):
        panel = tk.Frame(self.root, padx=10, pady=10)
        panel.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(panel, text="Seleccionar usuario:").pack(pady=5)
        self.selected_user = ttk.Combobox(panel, state="readonly", values=list(self.graph.adj_list.keys()))
        self.selected_user.pack()

        tk.Button(panel, text="Mostrar Información", command=self.show_info).pack(pady=10)

        tk.Label(panel, text="Conectar usuarios:").pack(pady=(10, 0))
        self.entry_user1 = ttk.Combobox(panel, state="readonly", values=list(self.graph.adj_list.keys()))
        self.entry_user2 = ttk.Combobox(panel, state="readonly", values=list(self.graph.adj_list.keys()))
        self.entry_user1.pack(pady=5)
        self.entry_user2.pack(pady=5)

        tk.Button(panel, text="Conectar Amigos", command=self.connect_users).pack(pady=10)

        self.output = tk.Text(panel, height=20, width=40)
        self.output.pack(pady=10)

    def generate_all_positions(self):
        for user in self.graph.adj_list:
            self.user_positions[user] = self.generate_position()

    def generate_position(self):
        while True:
            x, y = random.randint(50, 550), random.randint(50, 550)
            too_close = any(math.hypot(x - px, y - py) < 60 for px, py in self.user_positions.values())
            if not too_close:
                return x, y

    def draw_graph(self):
        self.canvas.delete("all")
        for user in self.graph.adj_list:
            for friend in self.graph.adj_list[user]:
                if user < friend:
                    x1, y1 = self.user_positions[user]
                    x2, y2 = self.user_positions[friend]
                    self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

        for user, (x, y) in self.user_positions.items():
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="#0d6efd", outline="")
            self.canvas.create_text(x, y, text=user, fill="white", font=("Arial", 10, "bold"))

    def connect_users(self):
        u1 = self.entry_user1.get()
        u2 = self.entry_user2.get()
        if u1 and u2 and u1 != u2:
            self.graph.add_friendship(u1, u2)
            self.draw_graph()
        else:
            messagebox.showwarning("Atención", "Selecciona dos usuarios diferentes para conectar.")

    def show_info(self):
        user = self.selected_user.get()
        if not user:
            messagebox.showwarning("Atención", "Selecciona un usuario.")
            return

        amigos = self.graph.get_friends(user)
        sugerencias = self.graph.suggest_friends_bfs(user)
        bfs_result = self.graph.bfs(user)
        dfs_result = self.graph.dfs(user)

        self.output.delete('1.0', tk.END)
        self.output.insert(tk.END, f"Amigos de {user}: {', '.join(amigos)}\n")
        self.output.insert(tk.END, f"Sugerencias (BFS nivel 2): {', '.join(sugerencias)}\n\n")
        self.output.insert(tk.END, f"Recorrido BFS desde {user}:\n{', '.join(bfs_result)}\n\n")
        self.output.insert(tk.END, f"Recorrido DFS desde {user}:\n{', '.join(dfs_result)}\n")

# ---------------- Ejecutar Programa ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SocialGraphApp(root)
    root.mainloop()
