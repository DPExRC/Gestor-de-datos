import tkinter as tk
from tkinter import ttk, messagebox

from components.botones import BotonBasePlace
from controller.AjustesController import AjustesController
from model.AjustesModel import AjustesModel
from view.DatosExcelView import DatosExcelView
from view.UnidadesView import UnidadesView
from view.RangosView import RangosView

class AjustesView:
    def __init__(self, root, volver_a_main_callback):
        self.root = root
        self.frame = tk.Frame(root)
        self.filters = []
        self.controller = None  # Iniciar sin controlador
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.volver_a_main_callback = volver_a_main_callback
            # Registro de vistas
        self.views = {}
        self.current_view = None
        self.logo =None
        
        self.create_widgets()

    def set_controller(self, controller):
        self.controller = controller

    def create_widgets(self):
         # Crear un contenedor principal
        self.frame.pack(fill="both", expand=True)

        # Insertar el logo
        self.logo = tk.PhotoImage(file="images/Imagen1.png")
        logo_label = tk.Label(self.frame, image=self.logo)
        logo_label.place(x=10, y=10, anchor="nw")

        # Crear título
        title_label = tk.Label(self.frame, text="Ajustes", font=("Arial", 24, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        # Botones
        estilo_boton = {"width": 20, "height": 2, "font": ("Arial", 12)}

        BotonBasePlace(
            self.frame,
            texto="Rangos",
            comando=self.mostrar_rangos_view,  # Asignar el método directamente
            rely=0.35,
            estilo_boton=estilo_boton
        )

        BotonBasePlace(
            self.frame,
            texto="Unidades",
            comando=self.mostrar_unidades_view,  # Asignar el método directamente
            rely=0.5,
            estilo_boton=estilo_boton
        )
        
        BotonBasePlace(
            self.frame,
            texto="Excel",
            comando=self.mostrar_datos_excel_view,  # Asignar el método directamente
            rely=0.65,
            estilo_boton=estilo_boton
        )

        BotonBasePlace(
            self.frame,
            texto="Volver",
            comando=self.volver_a_main_callback,  # Asignar el método directamente
            rely=0.85,
            estilo_boton=estilo_boton
        )
        



    def mostrar_rangos_view(self):
        """Mostrar la vista de Rangos."""
        self.hide()
        self.rangos_view = RangosView(self.root, self.show)
        self.rangos_view.show()

    def mostrar_unidades_view(self):
        """Mostrar la vista de Rangos."""
        self.hide()
        self.unidades_view = UnidadesView(self.root, self.show)
        self.unidades_view.show()

    def mostrar_datos_excel_view(self):
        """Mostrar la vista de Rangos."""
        self.hide()
        self.unidades_view = DatosExcelView(self.root, self.show)
        self.unidades_view.show()


# se necesitan en cada view, para mostrar y ocultar la vista
    def show(self):
        """Muestra la vista principal."""
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        """Oculta la vista principal."""
        self.frame.pack_forget()