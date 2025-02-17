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
        WithBoton = 20
        font = ("Arial", 10)

        botones_superiores = [
            ("Seleccionar archivo", self.select_file),
            ("Exportar a excel", self.export_to_excel),
            ("Guardar archivo", self.save_to_file),
            #("Exportar a Excel", self.export_to_excel),
            ("Volver", self.volver_a_main_callback),
        ]

        for i, (text, command) in enumerate(botones_superiores):
            btn = tk.Button(self.top_button_frame, text=text, command=command, width=WithBoton, font=font)
            btn.grid(row=0, column=i, padx=5)

        # --- MARCO FILTROS ---
        # Crear un LabelFrame para encerrar los filtros dentro de un rectángulo
        self.filter_container = tk.LabelFrame(self.frame, text="Filtros", font=("Arial", 10, "bold"))
        self.filter_container.pack(fill="x", pady=5, padx=5)

        # Crear el marco interno para organizar los filtros dentro del LabelFrame
        self.filter_frame = tk.Frame(self.filter_container)
        self.filter_frame.pack(fill="x", pady=1)


        # Encabezados de columnas para los filtros
        headers = ["LOCALIDAD", "PROGRAMA", "DIAS DE MUESTREO", "PUNTO MUESTREO", "ANALISIS"]

        self.filters = []

        for col, header in enumerate(headers):
            tk.Label(self.filter_frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)
            entry = tk.Entry(self.filter_frame, width=12)
            entry.grid(row=1, column=col, padx=5, pady=5, sticky="ew")
            self.filters.append(entry)

        # Botón Restablecer Filtros a la derecha del último entry
        btn_restablecer_filtros = tk.Button(
            self.filter_frame, text="Restablecer filtros", command=self.reset_filters,
            width=15, font=("Arial", 10)
        )
        btn_restablecer_filtros.grid(row=1, column=len(headers), padx=5, pady=5, sticky="w")


        # --- MARCO ACCIONES (BAJO FILTROS) ---
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(fill="x", pady=10)

                # Botones de acción
        acciones = [
            #("Restablecer filtros", self.reset_filters),
            ("Añadir fila", self.add_row),
            ("Eliminar fila", self.delete_row),
           # ("Vacios", self.vacios),
        ]

        # Generar los botones
        for i, (text, command) in enumerate(acciones):
            btn = tk.Button(self.button_frame, text=text, command=command, width=WithBoton, font=font)
            btn.grid(row=0, column=i, padx=5)  # Los botones ocupan las primeras columnas

        # Crear un marco para contener la tabla y la barra de desplazamiento
        self.table_container = tk.Frame(self.frame)
        self.table_container.pack(fill="both", expand=True)

        # Crear la tabla para mostrar datos
        self.tree = ttk.Treeview(self.table_container, show="headings")
        self.tree.bind("<Double-1>", self.start_edit)

        # Crear la barra de desplazamiento vertical
        self.scrollbar = ttk.Scrollbar(self.table_container, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Configurar la tabla para usar la barra de desplazamiento
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Empaquetar la tabla después de configurar la barra de desplazamiento
        self.tree.pack(side="left", fill="both", expand=True)


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

