from tkinter import filedialog, messagebox, ttk
import tkinter as tk

from openpyxl import load_workbook
import pandas as pd

from components.botones import BotonBasePlace
from controller.UnidadesController import UnidadesController
from model.UnidadesModel import UnidadesModel


class UnidadesView:
    def __init__(self, root, volver_a_ajustes_callback):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.volver_a_ajustes_callback = volver_a_ajustes_callback
        self.filters =  []
        self.modified_cells = set()
        self.current_file_path = None

        self.model = UnidadesModel()
        self.create_widgets()

        # Obtener los datos desde el modelo
        #self.headers, self.all_data = self.model.obtener_datos()
        self.headers, self.all_data = self.model.predeterminado()


        # Si los datos fueron obtenidos correctamente, actualizamos la tabla
        if self.headers and self.all_data:
            self.update_table(self.headers, self.all_data)
    
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

        # Depuración: Mostrar los datos originales
        print("Headers originales:", headers)
        print("Datos originales:")
        print(df)

        # Reemplazar valores NaN por cadenas vacías
        #df = df.dropna(axis=1, how='all')  # Eliminar columnas completamente vacías
        #df = df.fillna("0")  # Reemplazar NaN restantes con cadenas vacías

        # Depuración: Ver qué columnas se eliminaron
        print("Headers después de eliminar columnas vacías:", df.columns.tolist())
        print("Datos después del procesamiento:")
        print(df)

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
        self.top_frame = tk.Frame(self.frame, height=100)  
        self.top_frame.pack(fill="x", pady=10)
        self.top_frame.pack_propagate(False)  

        # Filtros
        self.entry_frame = tk.Frame(self.frame)
        self.entry_frame.pack(fill="x", pady=5, padx=10)

        headers = ["ANALISIS", "UNIDAD"]
        self.entry_fields = {}

        for i, header in enumerate(headers):
            label = tk.Label(self.top_frame, text=header, font=("Arial", 9, "bold"))
            label.grid(row=0, column=i, padx=5, pady=2)

            entry = tk.Entry(self.top_frame, width=15)
            entry.grid(row=1, column=i, padx=5, pady=2)
            self.entry_fields[header] = entry

        # Botones debajo de los filtros
        self.button_frame = tk.Frame(self.frame)
        self.button_frame.pack(fill="x", pady=5, padx=10)

        btn_guardar = tk.Button(
            self.button_frame, text="Guardar", command=self.export_to_excel,
            width=7, height=2, font=("Arial", 10)
        )
        btn_guardar.pack(side="left", padx=10, pady=5)

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

        #self.tree.bind("<Double-1>", self.start_edit)

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

        
    def start_edit(self, event=None):
        """Iniciar la edición de una celda seleccionada."""
        item = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        col_idx = int(col.replace("#", "")) - 1
        self.selected_row_idx = self.tree.index(item)
        self.selected_column = col_idx
        x, y, width, height = self.tree.bbox(item, column=col)
        value = self.tree.item(item)["values"][col_idx]
        
        self.current_entry = tk.Entry(self.tree)
        self.current_entry.insert(0, value)
        self.current_entry.place(x=x, y=y, width=width, height=height)
        self.current_entry.focus()
        self.current_entry.bind("<Return>", self.save_edit)
        self.current_entry.bind("<FocusOut>", self.cancel_edit)
        # Registrar la celda modificada
        self.modified_cells.add((self.selected_row_idx, self.selected_column))  # Usamos un set para evitar duplicados

    def save_edit(self, event=None):
        """Guardar la edición de una celda y actualizar 'FECHA DIGITACION' si corresponde."""
        if not self.current_entry:
            return

        new_value = self.current_entry.get().strip()
        item = self.tree.selection()[0]
        row_idx = self.tree.index(item)
        col_idx = self.selected_column

        # Actualizar en self.all_data
        self.all_data[row_idx][col_idx] = new_value  
        self.model.all_data[row_idx][col_idx] = new_value  # Asegurar que se refleje en el modelo

        # Guardar el nuevo valor en la tabla
        current_values = list(self.tree.item(item)["values"])
        current_values[col_idx] = new_value
        self.tree.item(item, values=current_values)

        self.is_data_modified = True  # Bandera de modificación
        self.modified_cells.add((row_idx, col_idx))  

        # Destruir la entrada
        if self.current_entry:
            self.current_entry.destroy()
            self.current_entry = None


    def cancel_edit(self, event=None):
        """Cancelar la edición y cerrar el Entry."""
        if self.current_entry:
            self.current_entry.destroy()
            self.current_entry = None

    def save_to_file(self):
            """Guardar los datos modificados en el archivo Excel en la ruta actual."""
            if not self.current_file_path:
                self.show_error("Error", "No hay archivo seleccionado.")
                return

            try:
                # Verificar si hay datos modificados
                if not self.is_data_modified:
                    self.show_warning("Advertencia", "No hay cambios para guardar.")
                    return

                # Verificar si hay filas con el valor "default" en alguna de sus celdas
                invalid_rows = [row for row in self.model.all_data if any("default" in str(cell).lower() for cell in row)]
                if invalid_rows:
                    self.show_warning("Advertencia", "No se puede guardar el archivo debido a valores 'default' en los datos.")
                    return

                # Exportar los datos al archivo base sobrescribiéndolo
                self.model.export_to_excel(self.model.all_data, self.model.headers, self.current_file_path)

                self.show_message("Éxito", f"Archivo guardado en {self.current_file_path}.")

                # Restablecer la bandera de modificación
                self.is_data_modified = False

            except Exception as e:
                self.show_error("Error al guardar archivo", str(e))



    def export_to_excel(self):
            """Exportar los datos a un archivo Excel"""
            file_path = "resources/Unidades.xlsx"

            if file_path:
                self.export(self.model.all_data, self.headers, file_path)
                self.show_message("Éxito", f"Datos exportados a {file_path}")

    def export(self, data, headers, file_path):
        """Exportar los datos modificados a un archivo Excel"""
        df = pd.DataFrame(self.model.all_data, columns=self.headers)  # Usar datos actualizados

        df.to_excel(file_path, index=False)

        wb = load_workbook(file_path)
        ws = wb.active

        for col in ws.columns:
            max_length = max(len(str(cell.value)) for cell in col if cell.value)
            column_letter = col[0].column_letter
            ws.column_dimensions[column_letter].width = max_length + 2

        wb.save(file_path)


    def show_message(self, title, message):
        """Muestra un mensaje de información."""
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        """Muestra un mensaje de advertencia."""
        messagebox.showwarning(title, message)
