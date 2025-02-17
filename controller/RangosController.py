import os
import sys
from tkinter import messagebox
from openpyxl import load_workbook
import pandas as pd
import tkinter as tk


class RangosController:
    def __init__(self, model, view, volver_a_ajustes_callback):
        self.model = model
        self.view = view
        self.volver_a_ajustes_callback = volver_a_ajustes_callback


        self.modified_cells = set()
        self.analysis_columns = {
            "DQO": "DQO",
            "ST": "ST",
            "SST": "SST",
            "SSV": "SSV",
            "PH": "ph",
            "AGV": "AGV (ácido acético)",
            "ALC": "alcalinidad (CaCO3)",
            "HUM": "% humedad",
            "TRAN": "transmitancia",
        }
        headers, all_data = self.model.predeterminado()


        # Si los datos fueron obtenidos correctamente, actualizamos la tabla
        if headers and all_data:

            self.view.update_table(headers, all_data)
        
        
        
        # Asociar el evento de "KeyRelease" a los campos de filtro para activar la actualización automática
        self.view.bind_filter_event(self.filter_data)

    def filter_data(self, event=None):
            """Filtrar los datos según las entradas en los filtros, manteniendo la correspondencia con sus índices originales."""
            # Obtener todos los datos e índices originales del modelo
            all_data = self.model.all_data

            # Aplicar cada filtro sobre los datos
            for col_idx, filter_entry in enumerate(self.view.filters):
                search_term = filter_entry.get().lower().strip()  # Obtener el término de búsqueda
                if search_term:
                    # Si hay un término para filtrar
                    all_data = [row for row in all_data if search_term in str(row[col_idx]).lower()]

            # Actualizar la tabla con los datos filtrados
            self.view.update_table(self.model.headers, all_data)

    def reset_filters(self):
        """Restablecer los filtros y mostrar todos los datos"""
        # Limpiar todos los filtros
        for filter_entry in self.view.filters:
            filter_entry.delete(0, tk.END)
        
        # Mostrar todos los datos
        self.view.update_table(self.model.headers, self.model.all_data)  # Mostrar todos los datos sin filtrar
   
            

    def save_edit(self, event=None):
            """Guardar la edición de una celda y actualizar 'FECHA DIGITACION' si corresponde."""
            if not self.current_entry:
                return

            headers = ["LOCALIDAD", "PUNTO MUESTREO", "ANALISIS", "MINIMO", "MAXIMO","UBICACION"]

            new_value = self.current_entry.get().strip()
            item = self.view.tree.selection()[0]
            col_idx = self.selected_column
            row_idx = self.selected_row_idx

            # Guardar el valor editado en el modelo de datos
            self.model.all_data[row_idx][col_idx] = new_value
            self.modified_cells.add((row_idx, col_idx))

            # Guardar el nuevo valor en la celda editada
            current_values = list(self.view.tree.item(item)["values"])
            current_values[col_idx] = new_value
            self.view.tree.item(item, values=current_values)

            row_index = self.view.tree.index(item)
            self.model.all_data[row_index] = current_values

            self.is_data_modified = True

            if self.current_entry:
                self.current_entry.destroy()
                self.current_entry = None

    def cancel_edit(self, event=None):
        """Cancelar la edición y cerrar el Entry."""
        if self.current_entry:
            self.current_entry.destroy()
            self.current_entry = None

    def start_edit(self, event=None):
        """Iniciar la edición de una celda seleccionada."""
        item = self.view.tree.selection()[0]
        col = self.view.tree.identify_column(event.x)
        col_idx = int(col.replace("#", "")) - 1
        self.selected_row_idx = self.view.tree.index(item)
        self.selected_column = col_idx

        x, y, width, height = self.view.tree.bbox(item, column=col)
        value = self.view.tree.item(item)["values"][col_idx]
        
        self.current_entry = tk.Entry(self.view.tree)
        self.current_entry.insert(0, value)
        self.current_entry.place(x=x, y=y, width=width, height=height)
        self.current_entry.focus()
        self.current_entry.bind("<Return>", self.save_edit)
        self.current_entry.bind("<FocusOut>", self.cancel_edit)

        # Registrar la celda modificada
        self.modified_cells.add((self.selected_row_idx, self.selected_column))  # Usamos un set para evitar duplicados

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

    def start_edit(self, event):
        """Iniciar la edición de una celda seleccionada."""


        item = self.view.tree.selection()[0]
        col = self.view.tree.identify_column(event.x)
        col_idx = int(col.replace("#", "")) - 1
        self.selected_row_idx = self.view.tree.index(item)
        self.selected_column = col_idx
        x, y, width, height = self.view.tree.bbox(item, column=col)
        value = self.view.tree.item(item)["values"][col_idx]
        
        self.current_entry = tk.Entry(self.view.tree)
        self.current_entry.insert(0, value)
        self.current_entry.place(x=x, y=y, width=width, height=height)
        self.current_entry.focus()
        self.current_entry.bind("<Return>", self.save_edit)
        self.current_entry.bind("<FocusOut>", self.cancel_edit)
        # Registrar la celda modificada
        self.modified_cells.add((self.selected_row_idx, self.selected_column))  # Usamos un set para evitar duplicados

    def get_path(self, filename):
        """Retorna la ruta persistente en 'resources' dentro de AppData."""
        base_dir = os.path.join(os.environ['APPDATA'], "SuralisLab", "resources")
        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, filename)

    def guardar_excel(self):
            """Exportar los datos a un archivo Excel"""
            file_path = self.get_path("Rangos.xlsx")

            if file_path:
                self.export(self.model.all_data, self.model.headers, file_path)
                self.show_message("Éxito", f"Datos guardados correctamente")


    def export(self, data, headers, file_path):
            """Exportar los datos a un archivo Excel"""

            #if not self.is_modified:
            #    print("No se ha realizado ningún cambio, no es necesario guardar.")
            #    return
            
            df = pd.DataFrame(data, columns=headers)

            if "ANÁLISIS" in df.columns:
                for key, column in self.analysis_columns.items():
                    df[column] = df["ANÁLISIS"].apply(
                        lambda x: next(
                            (val.strip() for val in str(x).split(",") if val.strip().upper() == key), None
                        )
                    )
                df = df.drop(columns=["ANÁLISIS"])
            
            if "MINIMO" in df.columns:
                df["MINIMO"] = pd.to_numeric(df["MINIMO"], errors="coerce")

            if "MAXIMO" in df.columns:
                df["MAXIMO"] = pd.to_numeric(df["MAXIMO"], errors="coerce")

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