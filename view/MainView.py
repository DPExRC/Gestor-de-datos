import tkinter as tk
from tkinter import filedialog  # Para seleccionar la ubicación del archivo
import pandas as pd

class MainView:
    def __init__(self, root, mostrar_vector_carga_callback, mostrar_resultados_excel_callback, 
                 mostrar_documentos_callback, mostrar_limites_callback):
        self.root = root
        self.frame = tk.Frame(root)
        self.mostrar_vector_carga_callback = mostrar_vector_carga_callback
        self.mostrar_resultados_excel_callback = mostrar_resultados_excel_callback
        self.mostrar_documentos_callback = mostrar_documentos_callback
        self.mostrar_limites_callback = mostrar_limites_callback
        self.logo = None
        self.current_file_path = None  # Ruta del archivo actual
        self.create_widgets()

    def create_widgets(self):
        self.frame.pack(fill="both", expand=True)

        # Insertar el logo (posición original)
        self.logo = tk.PhotoImage(file="images/Imagen1.png")
        logo_label = tk.Label(self.frame, image=self.logo)
        logo_label.place(x=10, y=10, anchor="nw")  # Logo en su posición original

        # Crear título centrado
        title_label = tk.Label(self.frame, text="Laboratorio Suralis", font=("Arial", 24, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")  # Centrado

        # Estilo de botones
        estilo_boton = {"width": 20, "height": 2, "font": ("Arial", 12)}

        # Crear botones
        self.boton_datos = tk.Button(self.frame, text="Datos", command=self.mostrar_resultados_excel_callback, **estilo_boton)
        self.boton_cp = tk.Button(self.frame, text="Programa CP", command=self.mostrar_vector_carga_callback, **estilo_boton)
        self.boton_despacho = tk.Button(self.frame, text="Despacho", command=self.mostrar_documentos_callback, **estilo_boton)
        self.boton_limites = tk.Button(self.frame, text="Ajustes", command=self.mostrar_limites_callback, **estilo_boton)

        # Posicionar los botones en una sola columna, centrados
        self.boton_datos.place(relx=0.5, rely=0.35, anchor="center")
        self.boton_cp.place(relx=0.5, rely=0.5, anchor="center")
        self.boton_despacho.place(relx=0.5, rely=0.65, anchor="center")
        self.boton_limites.place(relx=0.5, rely=0.8, anchor="center")



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
