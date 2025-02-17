import os
import sys
import tkinter as tk
from tkinter import messagebox

from components.get_path_images import get_path_images

class DocumentosView:
    def __init__(self, root, volver_a_main_callback):
        self.root = root
        self.controller = None
        self.frame = tk.Frame(root)
        self.volver_a_main_callback = volver_a_main_callback      
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.logo =None
        self.crear_widgets()



    def set_controller(self, controller):
        """Establece el controlador de la vista."""
        self.controller = controller

    def show(self):
        """Muestra la vista."""
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        """Oculta la vista."""
        self.frame.pack_forget()

    def show_message(self, title, message):
        """Muestra un mensaje."""
        messagebox.showinfo(title, message)


    def crear_widgets(self):
        """Crea los widgets principales."""
        # Logo
        self.logo = tk.PhotoImage(file=get_path_images("Imagen1.png"))
        logo_label = tk.Label(self.frame, image=self.logo)
        logo_label.image = self.logo  # Mantener referencia
        logo_label.place(x=10, y=10, anchor="nw")

        # Título
        title_label = tk.Label(self.frame, text="Tipo de documentación", font=("Arial", 24, "bold"))
        title_label.place(relx=0.5, rely=0.2, anchor="center")

        # Estilo de botones
        estilo_boton = {"width": 20, "height": 2, "font": ("Arial", 12)}
        anchor = "center"

        # Botones
        # Botón Caja
        self.boton_caja = tk.Button(self.frame, text="Etiqueta de caja", command=self.caja, **estilo_boton)
        self.boton_caja.place(relx=0.5, rely=0.35, anchor=anchor)

        # Botón Muestra
        self.boton_muestra = tk.Button(self.frame, text="Etiqueta de muestra", command=self.muestra, **estilo_boton)
        self.boton_muestra.place(relx=0.5, rely=0.5, anchor=anchor)

        # Botón Hoja de ruta
        self.boton_hoja_ruta = tk.Button(self.frame, text="Hoja de ruta", command=self.hoja_ruta, **estilo_boton)
        self.boton_hoja_ruta.place(relx=0.5, rely=0.65, anchor=anchor)

        # Botón Volver
        self.boton_volver = tk.Button(self.frame, text="Volver", command=self.volver_a_main_callback, **estilo_boton)
        self.boton_volver.place(relx=0.5, rely=0.85, anchor=anchor)

    def caja(self):
        """Evento del botón 'Caja'."""
        if self.controller:
            self.controller.handle_caja()

    def muestra(self):
        """Evento del botón 'Muestra'."""
        if self.controller:
            self.controller.handle_muestra()

    def hoja_ruta(self):
        """Evento del botón 'Hoja de ruta'."""
        if self.controller:
            self.controller.handle_hoja_ruta()
