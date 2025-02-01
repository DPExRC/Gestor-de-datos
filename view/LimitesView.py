import tkinter as tk
from tkinter import ttk, messagebox

class LimitesView:
    def __init__(self, root, volver_a_main_callback):
        self.root = root
        self.frame = tk.Frame(root)
        self.filters = []
        self.controller = None  # Iniciar sin controlador
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.volver_a_main_callback = volver_a_main_callback
        self.create_widgets()

    def set_controller(self, controller):
        self.controller = controller

    def create_widgets(self):
        # Título en la parte superior
        self.title_label = tk.Label(self.frame, text="Resultados Excel", font=("Helvetica", 16, "bold"))
        self.title_label.pack(pady=20)

        # Botón "Volver" debajo del título
        self.volver_a_main_callback_button = tk.Button(
            self.frame, text="Volver", command=self.volver_a_main_callback, width=20
        )
        self.volver_a_main_callback_button.pack(side="bottom", padx=5, pady=10)


# se necesitan en cada view, para mostrar y ocultar la vista
    def show(self):
        """Muestra la vista principal."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Oculta la vista principal."""
        self.frame.pack_forget()