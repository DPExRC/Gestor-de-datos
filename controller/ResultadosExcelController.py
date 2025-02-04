import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

from openpyxl import load_workbook
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
        self.cargar_archivo_predeterminado()

        # Asociar el evento de "KeyRelease" a los campos de filtro para activar la actualización automática
        self.view.bind_filter_event(self.filter_data)

    def cargar_archivo_predeterminado(self):
        """Método para cargar el archivo predeterminado desde los recursos"""


        try:
                file_path = self.leer_directorio()  # Obtiene la ruta del archivo desde directorios.txt
                
                if not file_path:
                    raise FileNotFoundError("No se encontró una ruta válida en directorios.txt")

                headers, data = self.model.load_file(file_path)
                self.view.update_table(headers, data, self.model.original_indices)
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
                    df.to_excel(file_path, index=False)
                    self.show_message("Éxito", f"Archivo guardado en: {file_path}")
                    self.guardar_directorio(file_path)
                    return file_path
        else:
                self.show_error("Error", "No hay datos para generar el archivo.")
        
        return headers, data
    
    def guardar_directorio(self, file_path):

        """Escribe contenido en un archivo.
        Args:
            ruta_archivo: La ruta al archivo donde se va a escribir.
            contenido: El texto que se va a escribir en el archivo.
        """

        try:
            with open("resources/directorios.txt", 'a') as f:  # Abre el archivo en modo escritura ('w')
                f.write(file_path + "\n")  # Escribe el contenido
            print(f"Se ha escrito en el archivo")
        except Exception as e:
            print(f"Error al escribir en el archivo: {e}")
        

    def leer_directorio(self):
        """Lee la última línea de un archivo de texto.

        Args:
            nombre_archivo: La ruta al archivo.

        Returns:
            La última línea del archivo (o None si el archivo está vacío o no existe).
        """
        try:
            with open("resources/directorios.txt", 'r') as f:
                lineas = f.readlines()
                if lineas:
                    return lineas[-1].strip()  # Elimina el salto de línea final
                else:
                    return None  # Archivo vacío
        except FileNotFoundError:
            return None  # Archivo no encontrado

    def vacios(self):
        """Muestra las filas donde las columnas 'FECHA RECEPCION', 'FECHA DIGITACION' y 'RESULTADO' están vacías o contienen NaN."""

        vacias = []
        headers = self.model.headers

        # Asegurarse de que las columnas requeridas existan
        try:
            fecha_recepcion_idx = headers.index("FECHA RECEPCION")
            fecha_digitacion_idx = headers.index("FECHA DIGITACION")
            resultado_idx = headers.index("RESULTADO")
        except ValueError:
            self.view.show_error("Error", "Las columnas 'FECHA RECEPCION', 'FECHA DIGITACION' o 'RESULTADO' no se encuentran en los datos.")
            return

        # Recorrer las filas y verificar si están vacías o contienen NaN
        for idx, row in enumerate(self.model.all_data):
            # Verificar si las celdas de las columnas específicas están vacías o contienen NaN
            fecha_recepcion_vacia = pd.isna(row[fecha_recepcion_idx]) or (isinstance(row[fecha_recepcion_idx], str) and row[fecha_recepcion_idx].strip() == "")
            fecha_digitacion_vacia = pd.isna(row[fecha_digitacion_idx]) or (isinstance(row[fecha_digitacion_idx], str) and row[fecha_digitacion_idx].strip() == "")
            
            # Para 'RESULTADO', verificamos si el valor es None, NaN o está vacío
            resultado_vacio = pd.isna(row[resultado_idx]) or (isinstance(row[resultado_idx], str) and row[resultado_idx].strip() == "") or (isinstance(row[resultado_idx], float) and row[resultado_idx] != row[resultado_idx])  # NaN check

            # Si las tres columnas están vacías o contienen NaN, agregar la fila a la lista de vacías
            if fecha_recepcion_vacia and fecha_digitacion_vacia and resultado_vacio:
                vacias.append(self.model.all_data[idx])

        # Si hay filas vacías, mostrarlas en la vista
        if vacias:
            self.view.update_table(self.model.headers, vacias)  # Actualiza la tabla con las filas vacías
            self.view.show_message("Filas vacías encontradas", f"Se han encontrado {len(vacias)} filas con fechas y resultados vacíos.")
        else:
            self.view.show_message("No hay filas vacías", "No se encontraron filas con fechas o resultados vacíos.")

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
                    if valor_float.is_integer():
                        new_value = int(valor_float)
                    else:
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
        """Guardar los datos modificados en el archivo Excel en la ruta actual."""
        if not self.current_file_path:
            self.view.show_error("Error", "No hay archivo seleccionado.")
            return

        try:
            # Verificar si hay datos modificados
            if not self.is_data_modified:
                self.view.show_warning("Advertencia", "No hay cambios para guardar.")
                return

            # Verificar si hay filas con el valor "default" en alguna de sus celdas
            invalid_rows = [row for row in self.model.all_data if any("default" in str(cell).lower() for cell in row)]
            if invalid_rows:
                self.view.show_warning("Advertencia", "No se puede guardar el archivo debido a valores 'default' en los datos.")
                return

            # Exportar los datos al archivo base sobrescribiéndolo
            self.model.export_to_excel(self.model.all_data, self.model.headers, self.current_file_path)

            self.view.show_message("Éxito", f"Archivo guardado en {self.current_file_path}.")

            # Restablecer la bandera de modificación
            self.is_data_modified = False

        except Exception as e:
            self.view.show_error("Error al guardar archivo", str(e))


    def filter_data(self, event=None):
        """Filtrar los datos según las entradas en los filtros, manteniendo la correspondencia con sus índices originales."""
        # Obtener todos los datos e índices originales del modelo
        all_data = self.model.all_data
        all_indices = self.model.original_indices  # Asegurarse de que exista esta lista en el modelo

        # Combinar datos e índices en una lista de tuplas
        paired = list(zip(all_data, all_indices))
        
        # Aplicar cada filtro sobre la lista de tuplas
        for col_idx, filter_entry in enumerate(self.view.filters):
            search_term = filter_entry.get().lower().strip()  # Obtener el término de búsqueda
            if search_term:  # Si hay un término para filtrar
                paired = [
                    (row, orig_idx) for row, orig_idx in paired
                    if search_term in str(row[col_idx]).lower()
                ]
        
        # Separar la lista filtrada en datos e índices
        filtered_data = [row for row, orig_idx in paired]
        filtered_indices = [orig_idx for row, orig_idx in paired]
        
        self.filtered_indices = filtered_indices  # Guardar los índices filtrados como un atributo

        # Actualizar la tabla con los datos e índices filtrados
        self.view.update_table(self.model.headers, filtered_data, filtered_indices)

    def reset_filters(self):
        """Restablecer los filtros y mostrar todos los datos"""
        # Limpiar todos los filtros
        for filter_entry in self.view.filters:
            filter_entry.delete(0, tk.END)
        
        # Mostrar todos los datos
        self.view.update_table(self.model.headers, self.model.all_data)  # Mostrar todos los datos sin filtrar
   
    def add_row(self):
        """Añadir una nueva fila con valores predeterminados en la posición deseada, usando los índices originales y actualizando el Treeview."""
        if not self.model.headers:
            tk.messagebox.showerror("Error", "No se puede añadir una fila sin datos cargados.")
            return

        # Crear una nueva fila con valores 'default'
        new_row = ["default"] * len(self.model.headers)

        try:
            # Obtener la fila seleccionada en el Treeview (índice filtrado)
            selected_item = self.view.tree.selection()[0]
            row_index = self.view.tree.index(selected_item)  # Índice en la tabla filtrada

            # Verificar si hay un filtro activo (existe filtered_indices)
            if hasattr(self, 'filtered_indices') and self.filtered_indices:
                original_indices = self.filtered_indices  # Asegurarse de que esta lista esté actualizada
                if row_index >= len(original_indices):
                    tk.messagebox.showerror("Error", "No se encontró la fila en el archivo original.")
                    return

                # Obtener el índice original de la fila seleccionada
                original_index = original_indices[row_index]  # Índice original en el archivo Excel
                # Encontrar el índice en los datos originales y agregar la fila
                original_data_index = self.model.original_indices.index(original_index)  # Obtener el índice en los datos originales
                self.model.all_data.insert(original_data_index + 1, new_row)  # Insertar la nueva fila después del índice original
                # Insertar el índice original correspondiente a la nueva fila
                self.model.original_indices.insert(original_data_index + 1, original_index + 1)  # Ajuste para el índice original

            else:
                # Si no hay filtro, insertar la fila después de la fila seleccionada
                if row_index >= len(self.model.all_data):
                    tk.messagebox.showerror("Error", "No se encontró la fila en la tabla.")
                    return

                self.model.all_data.insert(row_index + 1, new_row)
                new_index = self.model.original_indices[row_index] + 1  # Generar el nuevo índice después de la seleccionada
                self.model.original_indices.insert(row_index + 1, new_index)

            self.is_data_modified = True

        #except IndexError:
        #    tk.messagebox.showerror("Error", "Seleccione una fila para insertar la nueva fila después de ella.")

        except IndexError:
            # Si no hay ninguna fila seleccionada, añadir al final
            self.model.all_data.append(new_row)
            new_index = max(self.model.original_indices) + 1  # Generar el nuevo índice para el final
            self.model.original_indices.append(new_index)

        # Actualizar el Treeview con los datos completos (filtrados y originales)
        self.view.update_table(self.model.headers, self.model.all_data)

        # Si hay un filtro, actualizar los datos mostrados en el Treeview con la fila añadida
        if self.view.filters:
            self.filter_data()  # Filtrar los datos para reflejar la fila añadida en la vista filtrada

        tk.messagebox.showinfo("Éxito", "Nueva fila añadida correctamente.")



    def delete_rows_in_file(self, rows_to_delete):
        """
        Elimina las filas especificadas del archivo Excel original.

        Args:
            rows_to_delete (list): Lista de índices de fila a eliminar (1-indexados).
                Se recomienda omitir la fila de encabezados (por ejemplo, usar índices >=2).

        Returns:
            bool: True si la operación fue exitosa, False en caso de error.
        """
        try:
            # Obtiene la ruta del archivo desde directorios.txt
            file_path = self.leer_directorio()  
            # Imprimir la ruta del archivo base que se utilizará para eliminar filas
            print(f"Archivo base para eliminar filas: {file_path}")

            # Cargar el libro de Excel usando openpyxl
            wb = load_workbook(file_path)
            ws = wb.active

            # Ordenar los índices de filas a eliminar en orden descendente para evitar problemas de reindexación
            for row_idx in sorted(rows_to_delete, reverse=True):
                ws.delete_rows(row_idx)

            # Guardar el libro sobrescribiendo el archivo original
            wb.save(file_path)
            wb.close()
            return True
        except Exception as e:
            print(f"Error al eliminar filas en el archivo: {e}")
            return False

    #def delete_row(self):
    #    """Eliminar una fila seleccionada con confirmación y actualizar el archivo base."""
    #    try:
    #        # Obtener la fila seleccionada en el Treeview
    #        selected_item = self.view.tree.selection()[0]
    #        row_index = self.view.tree.index(selected_item)  # Índice en la tabla filtrada (TreeView/DataFrame)
    #        
    #        original_index = self.model.original_indices[row_index]  # Asegurarse de que exista esta lista en el modelo
#
    #        # Confirmación de eliminación
    #        confirm = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar esta fila?")
    #        if not confirm:
    #            return
    #        
    #        # Eliminar la fila del modelo y del TreeView
    #        # datos == default
    #        del self.model.all_data[row_index]
    #        del self.model.original_indices[row_index]
#
    #        # datos !== default
    #        del self.model.all_data[original_index]
    #        del self.model.original_indices[row_index]
    #        self.view.tree.delete(selected_item)
#
    #        # Intentar eliminar la fila en el archivo Excel
    #        if self.delete_rows_in_file([original_index]):  # Índice 1-based para Excel
    #            messagebox.showinfo("Éxito", "Fila eliminada correctamente del archivo base.")
    #        else:
    #            messagebox.showerror("Error", "No se pudo eliminar la fila del archivo base.")
#
    #        self.is_data_modified = True  # Marcar cambios
#
    #    except IndexError:
    #        messagebox.showerror("Error", "Por favor, selecciona una fila para eliminar.")



    def delete_row(self):
        """Eliminar las filas seleccionadas con confirmación y actualizar el archivo base."""
        try:
            # Obtener las filas seleccionadas en el Treeview
            selected_items = self.view.tree.selection()  # Devuelve una lista de los elementos seleccionados
            if not selected_items:
                messagebox.showerror("Error", "Por favor, selecciona al menos una fila para eliminar.")
                return

            # Confirmación de eliminación
            confirm = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar estas filas?")
            if not confirm:
                return

            # Ordenar las filas seleccionadas para asegurarse de eliminar desde el índice más alto
            # Esto es importante para evitar problemas al eliminar filas mientras se itera
            selected_items = sorted(selected_items, key=lambda item: self.view.tree.index(item), reverse=True)

            # Iterar sobre las filas seleccionadas para eliminar
            for selected_item in selected_items:
                row_index = self.view.tree.index(selected_item)  # Índice en la tabla filtrada (TreeView/DataFrame)

                # Asegurarse de que no se eliminen las filas de encabezado
                # Si row_index es menor que la longitud de los datos, eliminamos solo las filas de datos
                if row_index < len(self.model.all_data):
                    # Obtener el índice original del modelo
                    original_index = row_index  # Como no hay filtro, el índice filtrado es el mismo que el original

                    # Verificar si la fila contiene 'default'
                    row_dataframe = self.model.all_data[original_index]
                    if any("default" in str(cell).lower() for cell in row_dataframe):
                        # Si contiene 'default', eliminamos solo del DataFrame, no del archivo
                        del self.model.all_data[original_index]  # Eliminar de all_data
                        del self.model.original_indices[original_index]  # Eliminar el índice original
                        self.view.tree.delete(selected_item)  # Eliminar la fila del TreeView
                        messagebox.showinfo("Éxito", "Fila con 'default' eliminada solo del DataFrame.")
                    else:
                        # Eliminar los datos correspondientes de all_data
                        del self.model.all_data[original_index]  # Eliminar de all_data
                        del self.model.original_indices[original_index]  # Eliminar el índice original correspondiente

                        # Eliminar la fila del Treeview
                        self.view.tree.delete(selected_item)

                        # Intentar eliminar la fila en el archivo Excel
                        if self.delete_rows_in_file([original_index + 2]):  # Enviar índice ajustado para archivo Excel (1-based)
                            print(f"Fila {original_index + 2} eliminada correctamente del archivo base.")
                        else:
                            messagebox.showerror("Error", f"No se pudo eliminar la fila {original_index + 1} del archivo base.")
                            return  # Si falla la eliminación en el archivo Excel, no continuar

            messagebox.showinfo("Éxito", "Filas eliminadas correctamente.")
            self.is_data_modified = True  # Marcar que se realizaron modificaciones

        except IndexError:
            messagebox.showerror("Error", "Ocurrió un error al intentar eliminar las filas seleccionadas.")

    def delete_filtered_rows(self):
        """Eliminar todas las filas filtradas con confirmación."""
        if not self.filtered_indices:
            messagebox.showerror("Error", "No hay filas filtradas para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmación", "¿Deseas eliminar todas las filas filtradas?")
        if not confirm:
            return

        # Guardar índices originales antes de eliminar
        rows_to_delete = [self.filtered_indices[i] for i in range(len(self.filtered_indices))]

        # Eliminar del modelo
        for index in sorted(rows_to_delete, reverse=True):  # Eliminar en orden inverso para evitar errores
            del self.model.all_data[index]

        # Limpiar los índices filtrados y el TreeView
        self.filtered_indices.clear()
        self.view.tree.delete(*self.view.tree.get_children())

        # Intentar eliminar en el archivo Excel
        if self.delete_rows_in_file([i + 1 for i in rows_to_delete]):
            messagebox.showinfo("Éxito", "Todas las filas filtradas fueron eliminadas del archivo base.")
        else:
            messagebox.showerror("Error", "No se pudieron eliminar algunas filas del archivo base.")

        self.is_data_modified = True  # Marcar cambios

    def volver_a_main(self):
        """Método para volver a la vista principal."""
        self.volver_a_main_callback()
            
    def show_message(self, title, message):
        """Muestra un mensaje de información."""
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        """Muestra un mensaje de advertencia."""
        messagebox.showwarning(title, message)
