import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

import pandas as pd

from model import GeneradorModel

class ResultadosExcelController:
    def __init__(self, model, view, volver_a_main_callback):
        self.model = model
        self.view = view
        self.volver_a_main_callback = volver_a_main_callback

        self.selected_file = None
        self.is_data_modified = False
        self.current_entry = None
        self.selected_row_idx = None
        self.selected_column = None
        self.view.set_controller(self)
        self.current_file_path = None
        self.modified_cells = set()

        # Intentar cargar el archivo predeterminado al abrir la vista
        #self.cargar_archivo_predeterminado()

        # Asociar el evento de "KeyRelease" a los campos de filtro para activar la actualización automática
        self.view.bind_filter_event(self.filter_data)

    def cargar_archivo_predeterminado(self):
        """Método para cargar el archivo predeterminado desde los recursos"""
        headers, data = self.model.load_default_file()
        
        try:
            file_path = "resources/Libro2.xlsx"
            headers, data = self.model.load_file(file_path)
            self.view.update_table(headers, data)
            self.current_file_path = file_path
        except Exception as e:
            self.view.show_error("Error al cargar archivo", str(e))

    def select_file(self):
        """Abrir un cuadro de diálogo para seleccionar un archivo."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos Excel", ".xlsx"), ("Todos los archivos", ".*")]
        )

        try:
                headers, data = self.model.load_file(file_path)
                self.view.update_table(headers, data)
                self.current_file_path = file_path  # Actualiza la ruta del archivo actual
        except Exception as e:
                self.view.show_error("Error al cargar archivo", str(e))

    def load_file(self):
        """Muestra una tabla en Tkinter con solo los encabezados, sin cargar datos de un archivo."""
        headers = self.model.headers  # Obtener los encabezados definidos en el modelo
        self.view.update_table(headers, [])  # Llamar a la vista con una tabla vacía

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






    def generar_archivo_mensual_controller(self):        
        # Llamar a funciones específicas del modelo
        headers, data = self.model.loading_file()
        
        if headers and data:
                df = pd.DataFrame(data, columns=headers)
                nombre_mes = datetime.now().strftime("%B").upper()
                año = datetime.now().strftime("%Y")
                default_filename = f"{nombre_mes}_{año}.xlsx"
                
                directorio = filedialog.askdirectory(title="Seleccionar ubicación para guardar")
                if directorio:
                    file_path = f"{directorio}/{default_filename}"
                    print(f"file: {file_path} \n")
                    print(f"direc: {directorio}")

                    df.to_excel(file_path, index=False)
                    self.show_message("Éxito", f"Archivo guardado en: {file_path}")
        else:
                self.show_error("Error", "No hay datos para generar el archivo.")
        
        return headers, data

        
    def save_edit(self, event=None):
        """Guardar la edición de una celda y actualizar 'FECHA DIGITACION' si corresponde."""
        if not self.current_entry:
            return

        headers = ["PLANTA", "PUNTO MUESTREO", "FECHAS MUESTREO", "FECHA RECEPCION", "FECHA DIGITACION", "ANALISIS", "RESULTADO", "UNIDAD"]

        new_value = self.current_entry.get().strip()
        item = self.view.tree.selection()[0]
        col_idx = self.selected_column
        row_idx = self.selected_row_idx
        col_name = self.model.headers[col_idx]

        # Buscar índices de columnas
        if "RESULTADO" in headers and "FECHA DIGITACION" in headers:
            resultados_idx = headers.index("RESULTADO")
            fecha_digitacion_idx = headers.index("FECHA DIGITACION")

            # Si se edita "RESULTADO", actualizar "FECHA DIGITACION"
            if col_idx == resultados_idx:
                fecha_actual = datetime.now().strftime("%d/%m/%Y")  # Fecha en formato corto
                current_values = list(self.view.tree.item(item)["values"])
                current_values[fecha_digitacion_idx] = fecha_actual
                self.view.tree.item(item, values=current_values)

        # Validaciones para distintos tipos de datos
        if col_name in ["FECHAS MUESTREO", "FECHA RECEPCION", "FECHA DIGITACION"]:
            if new_value:  # Si hay un valor, validar formato de fecha
                try:
                    # Formato con slash
                    formato = "%d/%m/%Y %H:%M" if col_name == "FECHAS MUESTREO" else "%d/%m/%Y"
                    fecha = pd.to_datetime(new_value, format=formato, errors="coerce")

                    if pd.isna(fecha):
                        self.view.show_warning("Advertencia", f"Formato incorrecto en {col_name} (debe ser {formato.replace('%H:%M', 'HH:MM')})")
                        return
                    if col_name != "FECHAS MUESTREO":  # Si no es muestreo, guardamos solo la fecha sin hora
                        new_value = fecha.strftime("%d/%m/%Y")  # Convertimos a string con slash
                except Exception:
                    self.view.show_error("Error", f"Error al convertir {col_name}")
                    return
            else:  # Si está vacío, preguntar si desea guardar así
                respuesta = messagebox.askyesno(
                    "Confirmación", f"La celda en fila {row_idx + 1}, columna {col_name} está vacía.\n¿Desea guardarla así?"
                )
                if not respuesta:
                    return  # Cancelar guardado


        elif col_name == "RESULTADO":  # Validación de números decimales
            if new_value:  # Si hay un valor, validar número
                try:
                    valor_float = float(new_value)  # Guardar como número
                    new_value = round(valor_float, 6)  # Redondear a un máximo de 6 decimales sin forzar ceros innecesarios
                except ValueError:
                    self.view.show_warning("Advertencia", f"Formato incorrecto en {col_name} (debe ser un número decimal)")
                    return
            else:  # Si está vacío, preguntar si se quiere guardar
                respuesta = messagebox.askyesno(
                    "Confirmación", f"La celda en fila {row_idx + 1}, columna {col_name} está vacía.\n¿Desea guardarla así?"
                )
                if not respuesta:
                    return  # Cancelar guardado

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

    def export_to_excel(self):
        """Exportar los datos a un archivo Excel"""
        file_path = filedialog.asksaveasfilename(
            title="Guardar como",
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )

        if file_path:
            self.model.export_to_excel(self.model.all_data, self.model.headers, file_path)
            self.view.show_message("Éxito", f"Datos exportados a {file_path}")

    def save_to_file(self):
        """Guardar los datos modificados en el archivo Excel en una ubicación seleccionada por el usuario."""
        if not self.current_file_path:
            self.view.show_error("Error", "No hay archivo seleccionado.")
            return

        try:
            # Verificar si hay datos modificados
            if not self.is_data_modified:
                self.view.show_warning("Advertencia", "No hay cambios para guardar.")
                return

            # Verificar si hay filas inválidas (por ejemplo, con "default")
            invalid_rows = [row for row in self.model.all_data if "default" in row]
            if invalid_rows:
                self.view.show_warning("Advertencia", "Corrige los datos antes de guardar.")
                return

            # Convertir los datos a un DataFrame para validación
            df = pd.DataFrame(self.model.all_data, columns=self.model.headers)

            # Abrir cuadro de diálogo para guardar el archivo
            destination_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel Files", "*.xlsx")],
                title="Guardar como"
            )

            if not destination_path:
                self.view.show_error("Error", "No se seleccionó ninguna ubicación para guardar el archivo.")
                return

            # Exportar los datos a la ruta seleccionada
            self.model.export_to_excel(self.model.all_data, self.model.headers, destination_path)

            # Actualizar la ruta del archivo actual
            self.current_file_path = destination_path

            # Mostrar mensaje de éxito
            self.view.show_message("Éxito", f"Archivo guardado en {destination_path}.")

            # Restablecer el estado de modificación
            self.is_data_modified = False

        except Exception as e:
            self.view.show_error("Error al guardar archivo", str(e))

    def filter_data(self, event=None):
        """Filtrar los datos según las entradas en los filtros"""
        filtered_data = self.model.all_data  # Asumiendo que self.model.all_data contiene todos los datos

        # Filtrar por cada filtro
        for col_idx, filter_entry in enumerate(self.view.filters):
            search_term = filter_entry.get().lower().strip()  # Obtener el texto del filtro, sin espacios y en minúsculas
            if search_term:  # Si hay un término de búsqueda
                filtered_data = [
                    row for row in filtered_data
                    if search_term in str(row[col_idx]).lower()  # Comparar con la columna correspondiente
                ]

        # Actualizar la tabla con los datos filtrados
        self.view.update_table(self.model.headers, filtered_data)  # Asegúrate de pasar las cabeceras y los datos filtrados

    def reset_filters(self):
        """Restablecer los filtros y mostrar todos los datos"""
        # Limpiar todos los filtros
        for filter_entry in self.view.filters:
            filter_entry.delete(0, tk.END)
        
        # Mostrar todos los datos
        self.view.update_table(self.model.headers, self.model.all_data)  # Mostrar todos los datos sin filtrar

    def add_row(self):
        """Añadir una nueva fila con valores predeterminados en la posición deseada."""
        if not self.model.headers:
            tk.messagebox.showerror("Error", "No se puede añadir una fila sin datos cargados.")
            return

        # Crear una nueva fila con valores 'default'
        new_row = ["default"] * len(self.model.headers)

        try:
            # Obtener la fila seleccionada
            selected_item = self.view.tree.selection()[0]
            selected_index = self.view.tree.index(selected_item)  # Índice de la fila seleccionada

            # Insertar la nueva fila en los datos justo después de la fila seleccionada
            self.model.all_data.insert(selected_index + 1, new_row)
        except IndexError:
            # Si no hay ninguna fila seleccionada, añadir al final
            self.model.all_data.append(new_row)

        # Actualizar la tabla con los datos
        self.view.update_table(self.model.headers ,self.model.all_data)

        tk.messagebox.showinfo("Éxito", "Nueva fila añadida correctamente.")

    def delete_row(self):
        """Eliminar la fila seleccionada con confirmación."""
        try:
            # Obtener la fila seleccionada
            selected_item = self.view.tree.selection()[0]
            row_index = self.view.tree.index(selected_item)  # Índice de la fila seleccionada

            # Preguntar al usuario si está seguro de eliminar la fila
            confirm = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar esta fila?")
            if not confirm:
                return  # Cancelar eliminación si el usuario selecciona "No"

            # Eliminar la fila de los datos y del Treeview
            del self.model.all_data[row_index]
            self.view.tree.delete(selected_item)

            messagebox.showinfo("Éxito", "Fila eliminada correctamente.")
        except IndexError:
            messagebox.showerror("Error", "Por favor, selecciona una fila para eliminar.")

    def volver_a_main(self):
        """Método para volver a la vista principal."""
        self.volver_a_main_callback()