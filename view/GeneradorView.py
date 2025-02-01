from tkinter import filedialog, messagebox
import tkinter as tk
import pandas as pd

from components.botones import BotonBasePlace

class GeneradorView:
    def __init__(self, root, volver_a_main_callback):
        self.root = root
        self.frame = tk.Frame(root)
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

        # Crear un marco para los botones principales
        self.top_button_frame = tk.Frame(self.frame)
        self.top_button_frame.pack(fill="x", pady=5)

        estilo_boton = {"width": 20, "height": 2, "font": ("Arial", 12)}


        BotonBasePlace(
            self.frame,
            texto="Generar archivo",
            comando=self.generate_file,  # Asignar el método directamente
            rely=0.2,
            estilo_boton=estilo_boton
        )

        BotonBasePlace(
            self.frame,
            texto="Volver",
            comando=self.volver_a_main_callback,  # Asignar el método directamente
            rely=0.6,
            estilo_boton=estilo_boton
        )
        

    def generate_file(self):
        """Genera el archivo y permite al usuario guardarlo."""
        if self.controller:
            # Obtener los datos procesados del controlador
            headers, data = self.controller.get_processed_data()

            if headers and data:
                # Crear un DataFrame con los datos
                df = pd.DataFrame(data, columns=headers)

                # Abrir un cuadro de diálogo para guardar el archivo
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", ".xlsx"), ("All files", ".*")],
                    title="Guardar archivo generado"
                )

                if file_path:
                    # Exportar el DataFrame a Excel
                    df.to_excel(file_path, index=False)
                    self.show_message("Éxito", f"Archivo guardado en: {file_path}")
            else:
                self.show_error("Error", "No hay datos para generar el archivo.")

    def show_message(self, title, message):
        """Muestra un mensaje de información."""
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

# se necesitan OBLIGATORIAMENTE en cada view, para mostrar y ocultar la vista
    def show(self):
        """Muestra la vista principal."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Oculta la vista principal."""
        self.frame.pack_forget()