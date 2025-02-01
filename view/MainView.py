import tkinter as tk
from tkinter import ttk
from tkinter import filedialog  # Para seleccionar la ubicación del archivo
from components.botones import BotonBasePlace
import pandas as pd

class MainView:
    def __init__(self, root, mostrar_vector_carga_callback, mostrar_resultados_excel_callback, mostrar_documentos_callback, mostrar_rangos_callback): #mostrar_generador_callback):
        self.frame = tk.Frame(root)
        self.mostrar_vector_carga_callback = mostrar_vector_carga_callback
        self.mostrar_resultados_excel_callback = mostrar_resultados_excel_callback
        self.mostrar_documentos_callback = mostrar_documentos_callback
        self.mostrar_rangos_callback = mostrar_rangos_callback
        #self.mostrar_generador_callback = mostrar_generador_callback
        self.logo = None
        self.current_file_path = None  # Ruta del archivo actual
        self.create_widgets()

    def create_widgets(self):
        # Crear un contenedor principal
        self.frame.pack(fill="both", expand=True)

        # Insertar el logo
        self.logo = tk.PhotoImage(file="images/Imagen1.png")
        logo_label = tk.Label(self.frame, image=self.logo)
        logo_label.place(x=10, y=10, anchor="nw")

        # Crear título
        title_label = tk.Label(self.frame, text="Laboratorio Suralis", font=("Arial", 24, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        # Botones
        estilo_boton = {"width": 20, "height": 2, "font": ("Arial", 12)}

        #BotonBasePlace(
        #    self.frame,
        #    texto="Generar archivo mensual",
        #    comando=self.mostrar_generador_callback,  # Asignar el método directamente
        #    rely=0.2,
        #    estilo_boton=estilo_boton
        #)
        BotonBasePlace(
            self.frame,
            texto="Datos",
            comando=self.mostrar_resultados_excel_callback,  # Asignar el método directamente
            rely=0.35,
            estilo_boton=estilo_boton
        )
        BotonBasePlace(
            self.frame,
            texto="Programa CP",
            comando=self.mostrar_vector_carga_callback,
            rely=0.5,
            estilo_boton=estilo_boton
        )
        BotonBasePlace(
            self.frame,
            texto="Despacho",
            comando=self.mostrar_documentos_callback,
            rely=0.65,
            estilo_boton=estilo_boton
        )
        BotonBasePlace(
            self.frame,
            texto="Limites",
            comando=self.mostrar_rangos_callback,
            rely=0.8,
            estilo_boton=estilo_boton
        )

    def show(self):
        """Muestra la vista principal."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Oculta la vista principal."""
        self.frame.pack_forget()

    def select_file_path(self):
        """Seleccionar la ubicación del archivo."""
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        return file_path
    

    def export_to_excel(self, data, headers):
        """Exportar los datos a un archivo Excel."""
        df = pd.DataFrame(data, columns=headers)
        df.to_excel(self.current_file_path, index=False)
        print(f"Archivo guardado en: {self.current_file_path}")