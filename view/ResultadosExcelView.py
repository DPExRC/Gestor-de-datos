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
        self.controller = controller

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

        self.vacios = tk.Button(
            self.top_button_frame, text="Vacios", command=self.vacios, width=15
        )
        self.vacios.pack(side="left", padx=5)

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

        # Botón para disminuir semana
        self.disminuir_button = tk.Button(
            self.button_frame, text="-", command=self.print, width=5
        )
        self.disminuir_button.pack(side="left", padx=5)

        # Botón para aumentar semana
        self.aumentar_button = tk.Button(
            self.button_frame, text="+", command="", width=5
        )
        self.aumentar_button.pack(side="left", padx=5)

        # Crear un marco para contener la tabla y la barra de desplazamiento
        self.table_container = tk.Frame(self.frame)
        self.table_container.pack(fill="both", expand=True)

        # Crear la tabla para mostrar datos
        self.tree = ttk.Treeview(self.table_container, show="headings", selectmode='extended')
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

    def filtrar_semana_actual(self, data, headers):
        """Filtra los datos para incluir solo los de la semana actual, y si no está la fecha, muestra todas las semanas sin cambiar el orden."""
        try:
            if "FECHAS MUESTREO" not in headers:
                return data  

            fecha_idx = headers.index("FECHAS MUESTREO")
            df = pd.DataFrame(data, columns=headers)

            # Convertir columna de fechas a datetime
            df["FECHAS MUESTREO"] = pd.to_datetime(df["FECHAS MUESTREO"], dayfirst=True, errors="coerce")
            df = df.dropna(subset=["FECHAS MUESTREO"])  

            # Obtener la fecha de hoy y calcular la semana actual
            hoy = pd.Timestamp.today()
            primer_dia_mes = df["FECHAS MUESTREO"].min()
            ultimo_dia_mes = df["FECHAS MUESTREO"].max()
            primer_lunes = primer_dia_mes - pd.DateOffset(days=primer_dia_mes.weekday())
            semana_actual = ((hoy - primer_lunes).days // 7) + 1

            # Filtrar por la semana actual
            df["SEMANA"] = ((df["FECHAS MUESTREO"] - primer_lunes).dt.days // 7) + 1

            # Ajustar numeración: La primera semana con datos es la "Semana 1"
            semanas_unicas = sorted(df["SEMANA"].unique())
            mapa_semanas = {valor: idx + 1 for idx, valor in enumerate(semanas_unicas)}
            df["SEMANA"] = df["SEMANA"].map(mapa_semanas)

            if primer_dia_mes <= hoy <= ultimo_dia_mes:
                semana_hoy = ((hoy - primer_lunes).days // 7) + 1
                semana_hoy = mapa_semanas.get(semana_hoy, None)  # Ajustar a la numeración del archivo
            else:
                semana_hoy = None  # La fecha actual no está en el mes del archivo

            # Si la fecha de hoy no está en el archivo, mostrar todas las semanas sin alterar el orden
            if semana_hoy and semana_hoy in df["SEMANA"].values:
                df = df[df["SEMANA"] == semana_hoy]
            else:
                # No ordenar las filas, solo filtrar por semanas
                df = df  # No se realiza ninguna ordenación, se muestran todas las semanas

            # Reemplazar NaN en columnas específicas con ""
            columnas_a_reemplazar = ["FECHA RECEPCION", "FECHA DIGITACION", "UNIDAD"]
            for col in columnas_a_reemplazar:
                if col in df.columns:
                    df[col] = df[col].fillna("")

            return df[headers].values.tolist()
        
        except Exception as e:
            print(f"Error al filtrar la semana actual: {e}")
            return data  

    #def update_table(self, headers, data):
    #    """Actualiza la tabla con solo los datos de la semana actual y reemplaza NaN en ciertas columnas."""
#
    #    # Filtrar solo la semana actual o todas las semanas si la fecha de hoy no está en el archivo
    #    data_filtrada = self.filtrar_semana_actual(data, headers)
#
    #    self.tree.delete(*self.tree.get_children())
    #    self.tree["columns"] = list(range(len(headers)))
#
    #    column_widths = {
    #        "LOCALIDAD": 80,  # Ancho personalizado para la columna "LOCALIDAD"
    #        "PUNTO MUESTREO": 165,      # Ancho personalizado para la columna "FECHA"
    #        "FECHAS MUESTREO":115,
    #        }
#
    #    for idx, header in enumerate(headers):
    #        self.tree.heading(idx, text=header)
    #        self.tree.heading(idx, text=header)
#
    #        # Si la columna está en column_widths, se asigna el ancho personalizado
    #        if column_widths and header in column_widths:
    #            width = column_widths[header]
    #        else:
    #            width = 100  # Ancho por defecto
    #        self.tree.column(idx, width=width, anchor="center")
    #   
    #    try:
    #        resultado_idx = headers.index("RESULTADO")
    #    except ValueError:
    #        resultado_idx = None  
#
    #    for row in data_filtrada:
    #        formatted_row = list(row)  
#
    #        # Convertir las fechas a formato DD/MM/AAAA HH:MM
    #        for i, value in enumerate(formatted_row):
    #            if isinstance(value, str) or isinstance(value, datetime):
    #                try:
    #                    # Convertir a fecha con pandas
    #                    date_value = pd.to_datetime(value, errors='coerce')
    #                    if pd.notna(date_value):
    #                        formatted_row[i] = date_value.strftime('%d/%m/%Y %H:%M')
    #                except Exception:
    #                    pass  # Si no es una fecha válida, dejarlo como está

    def update_table(self, headers, data, original_indices=None):
        """
        Actualiza la tabla con datos proporcionados y ajusta los anchos de las columnas.
        Si se proporciona original_indices, se añade una columna extra llamada "ORIGINAL"
        que muestra el índice original de cada fila.
        """
        # Si se desea mostrar la columna de índices originales, agregarla a los encabezados
        if original_indices is not None:
            headers = headers.copy()  # Evitar modificar la lista original de encabezados
            headers.append("ORIGINAL")

        # Eliminar los elementos existentes en el Treeview
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(range(len(headers)))

        # Definir encabezados y ajustar anchos de columna
        for idx, header in enumerate(headers):
            self.tree.heading(idx, text=header)
            # Se puede ajustar el ancho según se desee; en este ejemplo, 100 para todas las columnas
            self.tree.column(idx, width=100, anchor="center")

        # Obtener el índice de la columna "RESULTADO" para formateo especial, si existe
        try:
            resultado_idx = headers.index("RESULTADO")
        except ValueError:
            resultado_idx = None

        # Insertar filas de datos en el Treeview
        for i, row in enumerate(data):
            formatted_row = list(row)  # Copiar la fila original

            # Si se proporcionó original_indices, agregar el valor correspondiente al final de la fila
            if original_indices is not None:
                formatted_row.append(original_indices[i])

            # Formateo especial para la columna "RESULTADO"
            if resultado_idx is not None:
                # Dado que se añadió una columna al final, el índice "resultado_idx" no varía
                value = formatted_row[resultado_idx]
                if pd.isna(value):
                    formatted_row[resultado_idx] = " "
                elif isinstance(value, float) and value.is_integer():
                    formatted_row[resultado_idx] = int(value)

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

    def vacios(self):
        if self.controller:
            self.controller.vacios()

    def generar_archivo_mensual(self):
        """Genera el archivo mensual con el nombre del mes y año actual y permite al usuario guardar en una ubicación."""
        if self.controller:
            self.controller.generar_archivo_mensual_controller()

    def reset_filters(self):
        if self.controller:
            self.controller.reset_filters()

    def print(self):
        if self.controller:
            self.controller.print_all_data()

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