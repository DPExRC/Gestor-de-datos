import tkinter as tk
from tkinter import filedialog 
import pandas as pd
from PIL import Image, ImageTk

from components.get_path_images import get_path_images


class MainView:
    def __init__(self, root, mostrar_vector_carga_callback, mostrar_resultados_excel_callback, 
                 mostrar_documentos_callback, mostrar_limites_callback, mostrar_rangos_callback,
                 mostrar_unidades_callback):
        self.root = root
        self.frame = tk.Frame(root)
        self.mostrar_vector_carga_callback = mostrar_vector_carga_callback
        self.mostrar_resultados_excel_callback = mostrar_resultados_excel_callback
        self.mostrar_documentos_callback = mostrar_documentos_callback
        self.mostrar_limites_callback = mostrar_limites_callback
        self.mostrar_rangos_callback = mostrar_rangos_callback
        self.mostrar_unidades_callback = mostrar_unidades_callback
        self.logo = None
        self.current_file_path = None  # Ruta del archivo actual
        self.create_widgets()

       

    def create_widgets(self):
        self.frame.pack(fill="both", expand=True)

        # Insertar el logo (posición original)
        self.logo = tk.PhotoImage(file=get_path_images("Imagen1.png"))
        logo_label = tk.Label(self.frame, image=self.logo)
        logo_label.place(x=10, y=10, anchor="nw")  # Logo en su posición original

        # Crear título centrado
        title_label = tk.Label(self.frame, text="Laboratorio Suralis", font=("Arial", 24, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")  # Centrado

        # Función para redimensionar imágenes
        def cargar_icono(ruta, ancho, alto):
            imagen = Image.open(get_path_images(ruta))  # Usar
            imagen = imagen.resize((ancho, alto), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(imagen)

        # Cargar imágenes
        icono_datos    = cargar_icono("datos.png", 40, 40)
        icono_datoscp  = cargar_icono("datoscp.png", 40, 40)
        icono_despacho = cargar_icono("despacho.png", 40, 40)
        icono_limites  = cargar_icono("ajustes.png", 40, 40)

        # Estilo de botones
        estilo_boton = {"width": 190, "height": 70, "compound": "left", "anchor": "w","font": ("Arial", 12)}

        # Crear botones con íconos
        self.boton_datos = tk.Button(
            self.frame, text="    DATOS", image=icono_datos,
            command=self.mostrar_resultados_excel_callback, **estilo_boton
        )
        self.boton_cp = tk.Button(
            self.frame, text="    PROGRAMA CP", image=icono_datoscp,
            command=self.mostrar_vector_carga_callback, **estilo_boton
        )
        self.boton_despacho = tk.Button(
            self.frame, text="    DESPACHO", image=icono_despacho,
            command=self.mostrar_documentos_callback, **estilo_boton
        )
        self.boton_limites = tk.Button(
            self.frame, text="    AJUSTES", image=icono_limites,
            command=self.mostrar_limites_callback, **estilo_boton
        )

        # Asegurarse de que las imágenes se mantengan referenciadas
        self.boton_datos.image = icono_datos
        self.boton_cp.image = icono_datoscp
        self.boton_despacho.image = icono_despacho
        self.boton_limites.image = icono_limites

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
