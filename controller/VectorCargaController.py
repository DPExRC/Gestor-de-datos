import tkinter as tk
from tkinter import filedialog, messagebox

import pandas as pd

from components.get_analisis import obtener_datos_analisis
from components.get_path_resources import get_path_resources
from components.show_messages import show_error, show_message, show_warning


class VectorCargaController:
    def __init__(self, model, view, volver_a_main_callback):
        self.model = model
        self.view = view
        self.volver_a_main_callback = volver_a_main_callback
        self.select_idx  = set()
        self.selecty_idx  = set()
        self.selected_idx  = set()

        self.selected_file = None
        self.is_data_modified = False
        self.current_entry = None
        self.selected_row_idx = None
        self.selected_column = None
        self.view.set_controller(self)
        self.current_file_path = None

        # Intentar cargar el archivo predeterminado al abrir la vista
        self.cargar_archivo_predeterminado()

        # Asociar el evento de "KeyRelease" a los campos de filtro para activar la actualización automática
        self.view.bind_filter_event(self.filter_data)
    

    def cargar_archivo_predeterminado(self):
        """Método para cargar el archivo predeterminado desde los recursos"""        
        try:
            file_path = get_path_resources("Libro2.xlsx")
            headers, data = self.model.load_file(file_path)

            # Lista de columnas permitidas
            columnas_permitidas = ['LOCALIDAD', 'PROGRAMA', 'DIAS DE MUESTRA', 'MUESTRA', 'ANALISIS', 'UBICACION']

            # Filtrar solo los índices de las columnas permitidas
            columnas_validas = [i for i, h in enumerate(headers) if h in columnas_permitidas]

            # Generar los nuevos encabezados y datos filtrados
            headers_filtrados = [headers[i] for i in columnas_validas]
            data_filtrada = [[row[i] for i in columnas_validas] for row in data]

            self.view.update_table(headers_filtrados, data_filtrada)
            self.current_file_path = file_path
            return headers_filtrados
        except Exception as e:
            show_error("Error al cargar archivo", str(e))

    def select_file(self):
        """Abrir un cuadro de diálogo para seleccionar un archivo."""
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )

        try:
                headers, data = self.model.load_file(file_path)
                self.view.update_table(headers, data)
                self.current_file_path = file_path  # Actualiza la ruta del archivo actual
        except Exception as e:
                show_error("Error al cargar archivo", str(e))


    def start_edit(self, event=None):
        """Iniciar la edición de una celda seleccionada."""
        item = self.view.tree.selection()[0]
        col = self.view.tree.identify_column(event.x)
        col_idx = int(col.replace("#", "")) - 1
        self.selected_row_idx = self.view.tree.index(item)
        self.selected_column = col_idx

        if col_idx == 4:
            self.show_analisis_window(item)
        else:    
            x, y, width, height = self.view.tree.bbox(item, column=col)
            value = self.view.tree.item(item)["values"][col_idx]

            self.current_entry = tk.Entry(self.view.tree)
            self.current_entry.insert(0, value)
            self.current_entry.place(x=x, y=y, width=width, height=height)
            self.current_entry.focus()
            self.current_entry.bind("<Return>", self.save_edit)
            self.current_entry.bind("<FocusOut>", self.cancel_edit)

    def show_analisis_window(self, item):
        """Mostrar una ventana emergente con los Checkbuttons para seleccionar análisis."""
        current_value = self.view.tree.item(item)["values"][self.selected_column]
        
        # Supongamos que los valores están separados por comas (ajusta según el formato real)
        selected_values = set(current_value.split(", "))  # Convierte a un conjunto para comparación exacta

        datos_analisis = obtener_datos_analisis()

        # Obtener las claves como lista
        claves = list(datos_analisis.keys())
                
        # Diccionario para almacenar el estado de cada Checkbutton
        self.checkbuttons_state = {}

        # Crear la ventana emergente
        analisis_window = tk.Toplevel(self.view.tree)
        analisis_window.title("SELECCIONAR ANÁLISIS")

        # Crear los Checkbuttons
        for analisis in claves:
            var = tk.BooleanVar()
            # Comparación exacta con los valores seleccionados
            if analisis in selected_values:
                var.set(True)
            self.checkbuttons_state[analisis] = var
            checkbutton = tk.Checkbutton(analisis_window, text=analisis, variable=var)
            checkbutton.pack(anchor="w")

        
        # Botón de Guardar
        save_button = tk.Button(analisis_window, text="Guardar", command=lambda: self.save_analisis_selection(item, analisis_window))
        save_button.pack()

    def save_analisis_selection(self, item, analisis_window):
        """Guardar las selecciones de análisis y actualizar la celda correspondiente."""
        # Crear una lista con los análisis seleccionados
        selected_analisis = [analisis for analisis, var in self.checkbuttons_state.items() if var.get()]
        # Convertir la lista de selección a un string, separando por comas
        new_value = ", ".join(selected_analisis)
        
        # Actualizar el valor en el Treeview y en el DataFrame
        self.view.tree.set(item, column=self.selected_column, value=new_value)
        row_data = list(self.model.all_data[self.selected_row_idx])
        row_data[self.selected_column] = new_value
        self.model.all_data[self.selected_row_idx] = row_data
        
        # Cerrar la ventana emergente
        analisis_window.destroy()

        # Notificar al usuario
        messagebox.showinfo("Éxito", "Análisis guardado correctamente.")

    def save_edit(self, event=None):
        """Guardar el valor editado en la celda."""
        new_value = self.current_entry.get()

        item = self.view.tree.selection()[0]
        col_idx=self.selected_column 
        current_values =self.view.tree.item(item)["values"]
        ##print(f"Fila en excel base: {current_values}")

        for idx, row in enumerate(self.model.all_data):

            # Comparar la fila seleccionada con cada fila en all_data
            if all(
                (value == selected_value or (pd.isna(value) and pd.isna(selected_value)))
                for value, selected_value in zip(row, current_values)
            ):
                self.selected_idx = idx
                ##print(f"Fila repetida encontrada en el índice de all_data: {idx}\nFila en excel: {idx+2}")
                ##print(f"tree: {current_values}\nall_data: {row}")

        # Actualizar el valor editado
        current_values[col_idx] = new_value
        self.view.tree.item(item, values=current_values)

                
        #row_data = list(self.model.all_data[self.selected_idx])
        #row_data[self.selected_column] = new_value
        self.model.all_data[self.selected_idx] =  current_values #row_data

        self.is_data_modified = True
        self.cancel_edit()

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
            show_message("Éxito", f"Datos exportados a {file_path}")

    def save_to_file(self):
        """Guardar los datos modificados en el archivo Excel"""
        if not self.current_file_path:
            show_error("Error", "No hay archivo seleccionado.")
            return


        try:
            # Ruta destino en resources
            destination_path = get_path_resources("Libro2.xlsx")
            destination_path2 = get_path_resources("Vector Carga.xlsx")
            self.model.export_to_excel(self.model.all_data, self.model.headers, self.current_file_path)
            self.model.export_to_excel2(self.model.all_data, self.model.headers, destination_path2)

            # Copiar y reemplazar el archivo en resources
            #shutil.copy(self.current_file_path, destination_path)
            
            #shutil.copy(destination_path, destination_path2)


        
            show_message("Éxito", f"Archivo guardado en {destination_path}.")
        except Exception as e:
            dp = destination_path.replace("\\","\\\\")
            if str(e) == f"'{dp}' and '{dp}' are the same file":
                pass
            elif str(e) == f"[Errno 13] Permission denied: '{dp}'":
                show_error("Error al guardar", f"No se puede guardar el archivo '{dp}' porque está abierto en otro programa. Ciérralo e intenta guardar de nuevo.")
            else:
                show_error("Error", str(e))



        invalid_rows = [row for row in self.model.all_data if "default" in row]
        if invalid_rows:
            show_warning("Advertencia", "Corrige los datos antes de guardar.")
            return

        self.model.export_to_excel(self.model.all_data, self.model.headers, self.current_file_path)
        show_message("Información", "Archivo guardado correctamente.")

    def filter_data(self, event=None):
        """Filtrar los datos según las entradas en los filtros"""
        filtered_data = self.model.all_data  # Asumiendo que `self.model.all_data` contiene todos los datos

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

        try:
            # Obtener la fila seleccionada
            selected_item = self.view.tree.selection()[0]
            selected_values = self.view.tree.item(selected_item)["values"]

            new_row = [f"(DEFAULT) {value}" for value in selected_values[:-1]] + [selected_values[-1]]

            for idx, row in enumerate(self.model.all_data):
                # Comparar la fila seleccionada con cada fila en all_data
                if all(
                    (value == selected_value or (pd.isna(value) and pd.isna(selected_value)))
                    for value, selected_value in zip(row, selected_values)
                ):
                    self.selecty_idx = idx
                    ##print(f"Fila repetida encontrada en el índice {idx}\nFila repetida encontrada en el índice real {idx+2}")
                    ##print(f"tree: {selected_values}\nall_data: {row}")

            selected_index = self.view.tree.index(selected_item)  # Índice de la fila seleccionada

            # Insertar la nueva fila en los datos justo después de la fila seleccionada
            self.model.all_data.insert(self.selecty_idx + 1, new_row)
        except IndexError:
            # Si no hay ninguna fila seleccionada, añadir al final
            self.model.all_data.append(new_row)

        # Guardar los valores de los filtros antes de actualizar la tabla
        current_filters = [entry.get() for entry in self.view.filters]

        # Actualizar la tabla con los datos
        self.view.update_table(self.model.headers, self.model.all_data)

        # Aplicar el filtro nuevamente
        self.apply_filters()

        tk.messagebox.showinfo("Éxito", "Nueva fila añadida correctamente.")


    def apply_filters(self, event=None):
        """Aplicar filtros según el valor de cada entrada."""
        filter_values = [entry.get() for entry in self.view.filters]
        
        # Filtrar los datos
        filtered_data = [
            row for row in self.model.all_data
            if all(
                (filter_value.lower() in str(value).lower() if filter_value else True)
                for filter_value, value in zip(filter_values, row)
            )
        ]
        
        # Actualizar la tabla con los datos filtrados
        self.view.update_table(self.model.headers, filtered_data)


            
    def delete_row(self):
        """Eliminar la fila seleccionada con confirmación."""
        try:
            # Obtener la fila seleccionada
            selected_item = self.view.tree.selection()[0]
            selected_values = self.view.tree.item(selected_item)["values"]
            for idx, row in enumerate(self.model.all_data):
                        # Comparar la fila seleccionada con cada fila en all_data
                        if all(
                            (value == selected_value or (pd.isna(value) and pd.isna(selected_value)))
                            for value, selected_value in zip(row, selected_values)
                        ):
                            self.select_idx = idx
                            ##print(f"Fila repetida encontrada en el índice {idx}\nFila repetida encontrada en el índice real {idx+2}")
                            ##print(f"tree: {selected_values}\nall_data: {row}")

            row_index = self.view.tree.index(selected_item)  # Índice de la fila seleccionada

            # Preguntar al usuario si está seguro de eliminar la fila
            confirm = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar esta fila?")
            if not confirm:
                return  # Cancelar eliminación si el usuario selecciona "No"

            # Eliminar la fila de los datos y del Treeview
            del self.model.all_data[self.select_idx]
            self.view.tree.delete(selected_item)

            messagebox.showinfo("Éxito", "Fila eliminada correctamente.")
        except IndexError:
            messagebox.showerror("Error", "Por favor, selecciona una fila para eliminar.")

    def volver_a_main(self):
        """Método para volver a la vista principal."""
        self.volver_a_main_callback()