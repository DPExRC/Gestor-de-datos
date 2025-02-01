import tkinter as tk
from tkinter import filedialog, messagebox
import shutil

from view.MainView import MainView


class VectorCargaController:
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

        # Intentar cargar el archivo predeterminado al abrir la vista
        self.cargar_archivo_predeterminado()

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
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )

        try:
                headers, data = self.model.load_file(file_path)
                self.view.update_table(headers, data)
                self.current_file_path = file_path  # Actualiza la ruta del archivo actual
        except Exception as e:
                self.view.show_error("Error al cargar archivo", str(e))

    def load_file(self):
        """Cargar datos del archivo Excel seleccionado y procesarlos"""
        if self.selected_file:
            headers, all_data = self.model.load_file(self.selected_file)
            self.view.update_table(headers, all_data)

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
        
        # Supongamos que tienes una lista de análisis disponibles
        available_analisis = self.analysis_columns = ["DQO", "ST", "SST", "SSV", "PH", "AGV", "ALC", "HUM", "TRAN"]
        
        # Creamos un diccionario para llevar el estado de cada Checkbutton
        self.checkbuttons_state = {}
        
        # Crear la ventana emergente
        analisis_window = tk.Toplevel(self.view.tree)
        analisis_window.title("Seleccionar ANÁLISIS")
        
        # Crear los Checkbuttons
        for analisis in available_analisis:
            var = tk.BooleanVar()
            # Si el análisis ya está en el valor actual, marcarlo como True
            if analisis in current_value:
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
        self.view.tree.set(self.view.tree.selection()[0], column=self.selected_column, value=new_value)

        row_data = list(self.model.all_data[self.selected_row_idx])
        row_data[self.selected_column] = new_value
        self.model.all_data[self.selected_row_idx] = row_data

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
            self.view.show_message("Éxito", f"Datos exportados a {file_path}")

    def save_to_file(self):
        """Guardar los datos modificados en el archivo Excel"""
        if not self.current_file_path:
            self.view.show_error("Error", "No hay archivo seleccionado.")
            return

        try:
            # Ruta destino en resources
            destination_path = "resources/Libro2.xlsx"
            
            self.model.export_to_excel(self.model.all_data, self.model.headers, self.current_file_path)
        
            # Copiar y reemplazar el archivo en resources
            shutil.copy(self.current_file_path, destination_path)
        
            self.view.show_message("Éxito", f"Archivo guardado en {destination_path}.")
        except Exception as e:
            self.view.show_error("Error al guardar archivo", str(e))

        invalid_rows = [row for row in self.model.all_data if "default" in row]
        if invalid_rows:
            self.view.show_warning("Advertencia", "Corrige los datos antes de guardar.")
            return

        self.model.export_to_excel(self.model.all_data, self.model.headers, self.current_file_path)
        self.view.show_message("Información", "Archivo guardado correctamente.")

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