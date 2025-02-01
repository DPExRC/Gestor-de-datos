import tkinter as tk
from tkinter import messagebox

class DocumentosView:
    def __init__(self, root, volver_a_main_callback):
        self.root = root
        self.controller = None
        self.frame = tk.Frame(root)
        self.volver_a_main_callback = volver_a_main_callback      
        self.frame.pack(fill=tk.BOTH, expand=True)
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
        logo = tk.PhotoImage(file="images/Imagen1.png")
        logo_label = tk.Label(self.frame, image=logo)
        logo_label.image = logo  # Mantener referencia
        logo_label.place(x=10, y=10, anchor="nw")

        # Título
        title_label = tk.Label(self.frame, text="Tipo de documentación", font=("Arial", 24))
        title_label.place(relx=0.5, y=20, anchor="n")

        # Botones
        # Botón Caja
        self.boton_caja = tk.Button(self.frame, text="Etiqueta de caja", command=self.caja, width=20, height=2, font=("Arial", 12))
        self.boton_caja.place(relx=0.5, rely=0.2, anchor="n")

        # Botón Muestra
        self.boton_muestra = tk.Button(self.frame, text="Etiqueta de muestra", command=self.muestra, width=20, height=2, font=("Arial", 12))
        self.boton_muestra.place(relx=0.5, rely=0.35, anchor="n")

        # Botón Hoja de ruta
        self.boton_hoja_ruta = tk.Button(self.frame, text="Hoja de ruta", command=self.hoja_ruta, width=20, height=2, font=("Arial", 12))
        self.boton_hoja_ruta.place(relx=0.5, rely=0.5, anchor="n")

        # Botón Volver
        self.boton_volver = tk.Button(self.frame, text="Volver", command=self.volver_a_main_callback, width=20, height=2, font=("Arial", 12))
        self.boton_volver.place(relx=0.5, rely=0.75, anchor="n")

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
