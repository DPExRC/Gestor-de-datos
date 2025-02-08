import pandas as pd
import tkinter as tk




class RangosController:
    def __init__(self):
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
        #self.view.bind_filter_event(self.filter_data)



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
            if search_term:
                  # Si hay un término para filtrar
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