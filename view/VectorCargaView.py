import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class VectorCargaView:
    def __init__(self, root, volver_a_main_callback):
        self.root = root
        self.frame = tk.Frame(root)
        self.filters = []
        self.controller = None  # Iniciar sin controlador
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.volver_a_main_callback = volver_a_main_callback
        self.create_widgets()

    def set_controller(self, controller):
        self.controller =controller

    def create_widgets(self):
        """Crea todos los widgets de la vista."""
        # Crear el marco para el área principal
        self.frame.pack(fill="both", expand=True)

        # Crear un marco para los botones arriba de los filtros
        self.top_button_frame = tk.Frame(self.frame)
        self.top_button_frame.pack(fill="x", pady=5)

        # Botón para cargar archivo
        self.load_button = tk.Button(
            self.top_button_frame, text="Seleccionar archivo", command=self.select_file, width=15
        )
        self.load_button.pack(side="left", padx=5)

        # Botón para exportar datos
        self.export_button = tk.Button(
            self.top_button_frame, text="Exportar a Excel", command=self.export_to_excel, width=15
        )
        self.export_button.pack(side="left", padx=5)

        # Botón para guardar archivo
        self.save_button = tk.Button(
            self.top_button_frame, text="Guardar archivo", command=self.save_to_file, width=15
        )
        self.save_button.pack(side="left", padx=5)

        self.volver_a_main_callback_button = tk.Button(
            self.top_button_frame, text="Volver", command=self.volver_a_main_callback, width=15
        )
        self.volver_a_main_callback_button.pack(side="left", padx=5)

        # Crear un marco para los filtros
        self.filter_frame = tk.Frame(self.frame)
        self.filter_frame.pack(fill="x", pady=5)

        # Encabezados de columnas para los filtros
        column_headers = ["LOCALIDAD", "PROGRAMA", "DIAS DE MUESTREO", "PUNTO MUESTREO", "ANÁLISIS"]

        # Crear etiquetas y entradas para los filtros
        for i, header in enumerate(column_headers):
            header_label = tk.Label(self.filter_frame, text=header)
            header_label.grid(row=0, column=i, padx=5, pady=5)  # Encabezados en la primera fila

            filter_entry = tk.Entry(self.filter_frame)
            filter_entry.grid(row=1, column=i, padx=5, pady=5)  # Entradas en la segunda fila
            self.filters.append(filter_entry)

        # Crear un marco para los botones de acción debajo de los filtros
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(fill="x", pady=10)

        # Botón para restablecer los filtros
        self.reset_button = tk.Button(
            self.button_frame, text="Restablecer filtros", command=self.reset_filters, width=15
        )
        self.reset_button.pack(side="left", padx=5)

        # Botón para añadir fila
        self.add_row_button = tk.Button(
            self.button_frame, text="Añadir fila", command=self.add_row, width=15
        )
        self.add_row_button.pack(side="left", padx=5)

        # Botón para eliminar fila
        self.delete_row_button = tk.Button(
            self.button_frame, text="Eliminar fila", command=self.delete_row, width=15
        )
        self.delete_row_button.pack(side="left", padx=5)

        # Crear la tabla para mostrar datos
        self.tree = ttk.Treeview(self.frame, show="headings")
        self.tree.bind("<Double-1>", self.start_edit)
        self.tree.pack(fill="both", expand=True, pady=5)

    def bind_filter_event(self, filter_function):
        """Vincula el evento de filtro en tiempo real."""
        for filter_entry in self.filters:
            filter_entry.bind("<KeyRelease>", filter_function)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))


    def update_table(self, headers, data):
        """Actualiza la tabla con datos proporcionados."""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(range(len(headers)))
        for idx, header in enumerate(headers):
            self.tree.heading(idx, text=header)
            self.tree.column(idx, width=100, anchor="center")

        for row in data:
            self.tree.insert("", "end", values=row)

    def show_message(self, title, message):
        """Muestra un mensaje de información."""
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        """Muestra un mensaje de advertencia."""
        messagebox.showwarning(title, message)

    def show(self):
        """Muestra esta vista."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Oculta esta vista."""
        self.frame.pack_forget()

    # Métodos temporales que delegan al controlador
    def select_file(self):
        if self.controller:
            self.controller.select_file()

    def reset_filters(self):
        if self.controller:
            self.controller.reset_filters()

    def add_row(self):
        if self.controller:
            self.controller.add_row()

    def delete_row(self):
        if self.controller:
            self.controller.delete_row()

    def export_to_excel(self):
        if self.controller:
            self.controller.export_to_excel()

    def save_to_file(self):
        if self.controller:
            self.controller.save_to_file()

    def start_edit(self, event):
        if self.controller:
            self.controller.start_edit(event)

