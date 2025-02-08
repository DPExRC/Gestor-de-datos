import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
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
        """Crea todos los widgets de la vista con mejor disposición visual."""
        
        # Marco principal expandible
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- MARCO SUPERIOR (BOTONES PRINCIPALES) ---
        self.top_button_frame = tk.Frame(self.frame)
        self.top_button_frame.pack(fill="x", pady=1)
        WithBoton = 20
        font = ("Arial", 10)

        botones_superiores = [
            ("Seleccionar archivo", self.select_file),
            ("Generar archivo mensual", self.generar_archivo_mensual),
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

        # Etiquetas de encabezado y entradas
        headers = [
            "LOCALIDAD", "PUNTO\nMUESTREO", "FECHA\nMUESTREO", "FECHA\nRECEPCION",
            "FECHA\nDIGITACION", "ANALISIS", "RESULTADO", "UNIDAD"
        ]

        self.filters = []

        for col, header in enumerate(headers):
            tk.Label(self.filter_frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)
            entry = tk.Entry(self.filter_frame, width=12)
            entry.grid(row=1, column=col, padx=5, pady=5, sticky="ew")
            self.filters.append(entry)


        # --- MARCO ACCIONES (BAJO FILTROS) ---
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(fill="x", pady=10)

        # --- Acción: Checkbox para seleccionar todas las filas visibles ---

        # Botones de acción
        acciones = [
            ("Restablecer filtros", self.reset_filters),
            #("Añadir fila", self.add_row),
            ("Eliminar fila", self.delete_row),
            ("Vacios", self.vacios),
        ]

        # Generar los botones
        for i, (text, command) in enumerate(acciones):
            btn = tk.Button(self.button_frame, text=text, command=command, width=WithBoton, font=font)
            btn.grid(row=0, column=i, padx=5)  # Los botones ocupan las primeras columnas

        # Checkbox para seleccionar todas las filas visibles
        self.select_all_var = tk.IntVar()  # Para el checkbox
        self.select_all_checkbox = tk.Checkbutton(self.button_frame, text="Seleccionar todo", variable=self.select_all_var, command=self.select_all_rows, font=font)
        self.select_all_checkbox.grid(row=0, column=len(acciones), padx=5)  # El checkbox se coloca justo después de "Vacios"


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

    def update_view(self, item, col_idx, new_value):
        """Actualizar solo una celda de la vista (interfaz gráfica) después de una edición."""
        current_values = list(self.view.tree.item(item)["values"])
        current_values[col_idx] = new_value
        self.view.tree.item(item, values=current_values)



    def update_table(self, headers, data, original_indices=None):
        """
        Actualiza la tabla con datos proporcionados y ajusta los anchos de las columnas.
        Si se proporciona original_indices, se añade una columna extra llamada "ORIGINAL"
        que muestra el índice original de cada fila.
        """

        # Configurar estilo para encabezados en negrita
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))#, padding = (1, 10))


        # Eliminar los elementos existentes en el Treeview
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(range(len(headers)))

        # Definir encabezados y ajustar anchos de columna
        for idx, header in enumerate(headers):
            self.tree.heading(idx, text=header,  anchor="center")  # Alineación centrada
            self.tree.column(idx, width=100,anchor="center")  # Ajustar ancho


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

            # Insertar la fila en el Treeview
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

    def select_all_rows(self):
        if self.controller:
            self.controller.select_all_rows()