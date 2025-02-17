
import tkinter as tk
from PIL import Image, ImageTk

from components.get_path_images import get_path_images


class AjustesView:
    def __init__(self, root, mostrar_rangos_callback, mostrar_unidades_callback, mostrar_directorios_callback, mostrar_main_view):
        self.root = root
        self.frame = tk.Frame(root)
        self.filters = []
        self.controller = None  
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.mostrar_main_view = mostrar_main_view
        self.mostrar_rangos_callback = mostrar_rangos_callback
        self.mostrar_unidades_callback = mostrar_unidades_callback
        self.mostrar_directorios_callback = mostrar_directorios_callback
        self.current_view = None
        self.logo =None

        
        self.create_widgets()
        

    def set_controller(self, controller):
        self.controller = controller

    def create_widgets(self):
         # Crear un contenedor principal
        self.frame.pack(fill="both", expand=True)

        # Insertar el logo
        self.logo = tk.PhotoImage(file=get_path_images("Imagen1.png"))
        logo_label = tk.Label(self.frame, image=self.logo)
        logo_label.place(x=10, y=10, anchor="nw")

        # Crear título
        title_label = tk.Label(self.frame, text="Ajustes", font=("Arial", 24, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        # Función para redimensionar imágenes
        def cargar_icono(ruta, ancho, alto):
            imagen = Image.open(get_path_images(ruta))  
            imagen = imagen.resize((ancho, alto), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(imagen)

        # Cargar imágenes
        icono_rangos      = cargar_icono("rangos.png", 40, 40)
        icono_unidades    = cargar_icono("unidades.png", 40, 40)
        icono_directorios = cargar_icono("directorios.png", 40, 40)
        icono_volver      = cargar_icono("volver.png", 40, 40)


        # Botones
        estilo_boton = {"width": 180, "height": 70, "compound": "left", "anchor": "w","font": ("Arial", 12)}

        self.boton_rangos = tk.Button(
            self.frame,
            text="        Rangos",
            image = icono_rangos,
            command=self.mostrar_rangos_callback,  
            **estilo_boton
        )

        self.boton_unidades = tk.Button(
            self.frame,
            text="        Unidades",
            image = icono_unidades,
            command=self.mostrar_unidades_callback,  
            **estilo_boton
        )

        self.boton_directorios = tk.Button(
            self.frame,
            text="        Directorios",
            image = icono_directorios,
            command=self.mostrar_directorios_callback,  
            **estilo_boton
        )

        self.boton_volver = tk.Button(
            self.frame,
            text="        Volver",
            image = icono_volver,
            command=self.mostrar_main_view,  # Asignar el método directamente            estilo_boton=estilo_boton
            **estilo_boton

        )
        
        # Asegurarse de que las imágenes se mantengan referenciadas
        self.boton_rangos.image = icono_rangos
        self.boton_unidades.image = icono_unidades
        self.boton_directorios.image = icono_directorios
        self.boton_volver.image = icono_volver

        # Posicionar los botones en una sola columna, centrados
        self.boton_rangos.place(relx=0.5, rely=0.35, anchor="center")
        self.boton_unidades.place(relx=0.5, rely=0.5, anchor="center")
        self.boton_directorios.place(relx=0.5, rely=0.65, anchor="center")
        self.boton_volver.place(relx=0.5, rely=0.8, anchor="center")

   


# se necesitan en cada view, para mostrar y ocultar la vista
    def show(self):
        """Muestra la vista principal."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Oculta la vista principal."""
        self.frame.pack_forget()