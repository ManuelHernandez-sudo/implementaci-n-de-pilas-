import tkinter as tk
from tkinter import messagebox

class DoublyNode:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_node = None

    def append(self, value):
        new_node = DoublyNode(value)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current_node = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            self.current_node = new_node

    def move_forward(self):
        if self.current_node and self.current_node.next:
            self.current_node = self.current_node.next

    def move_backward(self):
        if self.current_node and self.current_node.prev:
            self.current_node = self.current_node.prev

    def current(self):
        return self.current_node.value if self.current_node else None

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto")
        
        self.text_area = tk.Text(root, wrap='word', height=15, width=50)
        self.text_area.pack(pady=10)

        self.history = DoublyLinkedList()
        
        self.save_button = tk.Button(root, text="Guardar estado", command=self.save_state)
        self.save_button.pack(side='left', padx=5)

        self.undo_button = tk.Button(root, text="Deshacer", command=self.undo)
        self.undo_button.pack(side='left', padx=5)

        self.redo_button = tk.Button(root, text="Rehacer", command=self.redo)
        self.redo_button.pack(side='left', padx=5)

    def save_state(self):
        current_text = self.text_area.get("1.0", tk.END).strip()
        self.history.append(current_text)
        messagebox.showinfo("Estado guardado", "El estado del texto ha sido guardado.")

    def undo(self):
        self.history.move_backward()
        current_text = self.history.current()
        if current_text is not None:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, current_text)

    def redo(self):
        self.history.move_forward()
        current_text = self.history.current()
        if current_text is not None:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, current_text)

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()