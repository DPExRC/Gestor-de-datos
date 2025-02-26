from tkinter import messagebox, ttk
import tkinter as tk
import pandas as pd


class UnidadesView:
    def __init__(self, root, volver_a_ajustes_callback):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.volver_a_ajustes_callback = volver_a_ajustes_callback
        self.filters =  []
        self.modified_cells = set()

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

        # Botones debajo de los filtros
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(fill="x", pady=5, padx=10)

        estilo_boton = {"width": 12, "height": 2, "font": ("Arial", 10)}

        btn_guardar = tk.Button(
            self.button_frame, text="Guardar", command=self.export_to_excel,
            **estilo_boton
        )
        btn_guardar.pack(side="left", padx=10, pady=5)
        

        btn_add_analisis = tk.Button(
            self.button_frame, text="Añadir analisis", command=self.add_analisis,
            **estilo_boton
        )
        btn_add_analisis.pack(side="left", padx=10, pady=5)

        btn_delete_analisis = tk.Button(
            self.button_frame, text="Borrar analisis", command=self.delete_analisis,
            **estilo_boton
        )
        btn_delete_analisis.pack(side="left", padx=10, pady=5)

        btn_volver = tk.Button(
            self.button_frame, text="Volver", command=self.volver_a_limites,
            **estilo_boton
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


    def bind_filter_event(self, filter_function):
        """Vincula el evento de filtro en tiempo real."""
        for filter_entry in self.filters:
            filter_entry.bind("<KeyRelease>", filter_function)

    def volver_a_limites(self):
        """Vuelve a la vista de límites.""" 
        self.hide()
        self.volver_a_ajustes_callback()

    def add_analisis(self):
        if self.controller:
            self.controller.add_row()

    def delete_analisis(self):
        if self.controller:
            self.controller.delete_row()

    def show(self):
        """Muestra esta vista."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Oculta esta vista."""
        self.frame.pack_forget()

    def actualizar(self):
        """Actualiza datos"""
        if self.controller:
            self.controller.actualizar()
        
    def start_edit(self, event=None):
        if self.controller:
            self.controller.start_edit(event)      

    def save_edit(self, event=None):
        if self.controller:
            self.controller.save_edit()


    def cancel_edit(self, event=None):
        if self.controller:
            self.controller.cancel_edit()

    def save_to_file(self):
        if self.controller:
            self.controller.save_to_file()



    def export_to_excel(self):
        if self.controller:
            self.controller.export_to_excel()




    def show_message(self, title, message):
        """Muestra un mensaje de información."""
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        """Muestra un mensaje de advertencia."""
        messagebox.showwarning(title, message)