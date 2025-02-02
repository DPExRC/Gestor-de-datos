from datetime import datetime
import re
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog

import pandas as pd
import calendar
import locale


# Configurar el idioma local a español para los nombres de los meses
#locale.setlocale(locale.LC_TIME, 'es_ES.utf8')  # Para Linux y Mac
locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Para Windows, si es necesario


class ResultadosExcelView:
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

        # Botón para generar archivo
        self.generar_archivo_mensual_button = tk.Button(
            self.top_button_frame, text="Generar archivo mensual", command=self.generar_archivo_mensual, width=20
        )
        self.generar_archivo_mensual_button.pack(side="left", padx=5)

        # Botón para guardar archivo
        self.save_button = tk.Button(
            self.top_button_frame, text="Guardar archivo", command=self.save_to_file, width=15
        )
        self.save_button.pack(side="left", padx=5)

        # Botón para exportar datos
        self.export_button = tk.Button(
            self.top_button_frame, text="Exportar a Excel", command=self.export_to_excel, width=15
        )
        self.export_button.pack(side="left", padx=5)

        self.volver_a_main_callback_button = tk.Button(
            self.top_button_frame, text="Volver", command=self.volver_a_main_callback, width=15
        )
        self.volver_a_main_callback_button.pack(side="left", padx=5)

        # Crear un marco para los filtros
        self.filter_frame = tk.Frame(self.frame)
        self.filter_frame.pack(fill="x", pady=5)




        # Crear etiquetas y entradas para los filtros
        header_label_0 = tk.Label(self.filter_frame, text="LOCALIDAD")
        header_label_0.grid(row=0, column=0, padx=5, pady=5)
        filter_entry_0 = tk.Entry(self.filter_frame, width=5)
        filter_entry_0.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.filters.append(filter_entry_0)

        header_label_1 = tk.Label(self.filter_frame, text="PUNTO\nMUESTREO")
        header_label_1.grid(row=0, column=1, padx=5, pady=5)
        filter_entry_1 = tk.Entry(self.filter_frame, width=5)
        filter_entry_1.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.filters.append(filter_entry_1)

        header_label_2 = tk.Label(self.filter_frame, text="FECHAS\nMUESTREO")
        header_label_2.grid(row=0, column=2, padx=5, pady=5)
        filter_entry_2 = tk.Entry(self.filter_frame, width=5)
        filter_entry_2.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.filters.append(filter_entry_2)

        header_label_3 = tk.Label(self.filter_frame, text="FECHA\nRECEPCION")
        header_label_3.grid(row=0, column=3, padx=5, pady=5)
        filter_entry_3 = tk.Entry(self.filter_frame, width=5)
        filter_entry_3.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.filters.append(filter_entry_3)

        header_label_4 = tk.Label(self.filter_frame, text="FECHA\nDIGITACION")
        header_label_4.grid(row=0, column=4, padx=5, pady=5)
        filter_entry_4 = tk.Entry(self.filter_frame, width=5)
        filter_entry_4.grid(row=1, column=4, padx=5, pady=5, sticky="ew")
        self.filters.append(filter_entry_4)

        header_label_5 = tk.Label(self.filter_frame, text="ANALISIS")
        header_label_5.grid(row=0, column=5, padx=5, pady=5)
        filter_entry_5 = tk.Entry(self.filter_frame, width=5)
        filter_entry_5.grid(row=1, column=5, padx=5, pady=5, sticky="ew")
        self.filters.append(filter_entry_5)

        header_label_6 = tk.Label(self.filter_frame, text="RESULTADO")
        header_label_6.grid(row=0, column=6, padx=5, pady=5)
        filter_entry_6 = tk.Entry(self.filter_frame, width=5)
        filter_entry_6.grid(row=1, column=6, padx=5, pady=5, sticky="ew")
        self.filters.append(filter_entry_6)

        header_label_7 = tk.Label(self.filter_frame, text="UNIDAD")
        header_label_7.grid(row=0, column=7, padx=5, pady=5)
        filter_entry_7 = tk.Entry(self.filter_frame, width=5)
        filter_entry_7.grid(row=1, column=7, padx=5, pady=5, sticky="ew")
        self.filters.append(filter_entry_7)


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

        #self.tree.bind("<ButtonRelease-1>", self.on_item_click)


    def bind_filter_event(self, filter_function):
        """Vincula el evento de filtro en tiempo real."""
        for filter_entry in self.filters:
            filter_entry.bind("<KeyRelease>", filter_function)

    def update_table(self, headers, data):
        """Actualiza la tabla con datos proporcionados y ajusta los anchos de las columnas según lo especificado."""
        
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(range(len(headers)))

        # Definir encabezados y ajustar anchos de columna
        for idx, header in enumerate(headers):
            self.tree.heading(idx, text=header)
            self.tree.column(idx, width=100, anchor="center")

        # Obtener el índice de la columna "RESULTADO"
        try:
            resultado_idx = headers.index("RESULTADO")
        except ValueError:
            resultado_idx = None  # Si no existe la columna, evitar error

        # Insertar filas de datos con formato corregido solo en "RESULTADO"
        for row in data:
            formatted_row = list(row)  # Copiar la fila original
            if resultado_idx is not None:
                value = formatted_row[resultado_idx]
                if isinstance(value, float) and value.is_integer():
                    formatted_row[resultado_idx] = int(value)  # Convertir 45.0 → 45
            self.tree.insert("", "end", values=formatted_row)



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

    def generar_archivo_mensual(self):
        """Genera el archivo mensual con el nombre del mes y año actual y permite al usuario guardar en una ubicación."""
        if self.controller:
            self.controller.generar_archivo_mensual_controller()

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

