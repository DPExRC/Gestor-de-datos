from tkinter import  messagebox, ttk
import tkinter as tk
import pandas as pd



class RangosView:
    def __init__(self, root, volver_a_ajustes_callback):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.volver_a_ajustes_callback = volver_a_ajustes_callback
        self.filters =  []
     
        self.current_file_path = None

        self.create_widgets()

    
    def set_controller(self, controller):
        self.controller = controller

    def update_table(self, headers, all_data):
        """
        Muestra los headers y all_data en un Treeview, omitiendo columnas con valores NaN.
        """
        # Limpiar cualquier dato previo en la tabla
        self.tree.delete(*self.tree.get_children())

        # Convertir a DataFrame para manipulación de datos
        df = pd.DataFrame(all_data, columns=headers)

        # Reemplazar valores NaN por cadenas vacías
        #df = df.dropna(axis=1, how='all')  # Eliminar columnas completamente vacías
        df = df.fillna("")  # Reemplazar NaN restantes con cadenas vacías

        # Actualizar headers y all_data sin valores NaN
        headers = df.columns.tolist()
        all_data = df.values.tolist()

        # Configurar las columnas con los headers
        self.tree["columns"] = headers

        # Crear las cabeceras de la tabla
        for header in headers:
            self.tree.heading(header, text=header)  # Configurar el encabezado
            self.tree.column(header, width=80, anchor="center")  # Configurar la columna

        # Insertar los datos en las filas
        for row in all_data:
            self.tree.insert("", "end", values=row)

    def create_widgets(self):
        self.top_frame = tk.Frame(self.frame)  
        self.top_frame.pack(fill="x")
        self.top_frame.pack_propagate(False)  

        # --- MARCO FILTROS ---
        # Crear un LabelFrame para encerrar los filtros dentro de un rectángulo
        self.filter_container = tk.LabelFrame(self.frame, text="Filtros", font=("Arial", 10, "bold"))
        self.filter_container.pack(fill="x", pady=0, padx=5)

        # Filtros
        self.filter_frame = tk.Frame(self.filter_container)
        self.filter_frame.pack(fill="x", pady=0)

        headers = ["LOCALIDAD", "MUESTRA", "ANALISIS", "MINIMO", "MAXIMO","UBICACION"]
        self.filters = []

        for col, header in enumerate(headers):
            tk.Label(self.filter_frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)
            entry = tk.Entry(self.filter_frame, width=12)
            entry.grid(row=1, column=col, padx=5, pady=5, sticky="ew")
            self.filters.append(entry)

        # Botón Restablecer Filtros a la derecha del último entry
        btn_restablecer_filtros = tk.Button(
            self.filter_frame, text="Restablecer filtros", command=self.restablecer_filtros,
            width=15, font=("Arial", 10)
        )
        btn_restablecer_filtros.grid(row=1, column=len(headers), padx=5, pady=5, sticky="w")

        # Botones debajo de los filtros
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(fill="x", pady=5, padx=10)

        btn_guardar = tk.Button(
            self.button_frame, text="Guardar", command=self.guardar_excel,
            width=7, height=2, font=("Arial", 10)
        )
        btn_guardar.pack(side="left", padx=10, pady=5)

        btn_actualizar = tk.Button(
            self.button_frame, text="Actualizar", command=self.actualizar_datos,
            width=7, height=2, font=("Arial", 10)
        )
        btn_actualizar.pack(side="left", padx=10, pady=5)

        btn_ubicaciones = tk.Button(
            self.button_frame, text="Generar UBICACIONES", command=self.ubicaciones,
            width=7, height=2, font=("Arial", 10)
        )
        btn_ubicaciones.pack(side="left", padx=10, pady=5)


        btn_volver = tk.Button(
            self.button_frame, text="Volver", command=self.volver_a_limites,
            width=7, height=2, font=("Arial", 10)
        )
        btn_volver.pack(side="left", padx=10, pady=5)


        self.table_frame = tk.Frame(self.frame)
        self.table_frame.pack(pady=5, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(self.table_frame, show="headings", selectmode='extended')
        self.tree.bind("<Double-1>", self.start_edit)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)  

        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)


    def ubicaciones(self):
        print("Hola1")
        if self.controller:
            self.controller.ubicaciones()

    def restablecer_filtros(self):
        if self.controller:
            self.controller.reset_filters()

    def actualizar_datos(self):
        self.controller.actualizar_datos()

    def guardar_excel(self):
        if self.controller:
            self.controller.guardar_excel()

    def bind_filter_event(self, filter_function):
        """Vincula el evento de filtro en tiempo real."""
        for filter_entry in self.filters:
            filter_entry.bind("<KeyRelease>", filter_function)

    def volver_a_limites(self):
        """Vuelve a la vista de límites.""" 
        self.hide()
        self.volver_a_ajustes_callback()

    def show(self):
        """Muestra esta vista."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Oculta esta vista."""
        self.frame.pack_forget()

        
    def start_edit(self, event):
        if self.controller:
            self.controller.start_edit(event)

    def save_edit(self, event=None):
        if self.controller:
            self.controller.save_edit()

    def cancel_edit(self, event=None):
        if self.controller:
            self.controller.cancel_edit()

    def save_edit(self, event=None):
        if self.controller:
            self.controller.save_edit()

   

    def show_message(self, title, message):
        """Muestra un mensaje de información."""
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        """Muestra un mensaje de advertencia."""
        messagebox.showwarning(title, message)