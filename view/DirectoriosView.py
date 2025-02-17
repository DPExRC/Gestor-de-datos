import tkinter as tk

class DirectoriosView:
    def __init__(self, root, volver_a_ajustes_callback):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.volver_a_ajustes_callback = volver_a_ajustes_callback
        self.create_widgets()


    def set_controller(self, controller):
        """Establece el controlador de la vista."""
        self.controller = controller
        self.defaults()


    def create_widgets(self):
        
        # Frame superior para los botones
        self.top_frame = tk.Frame(self.frame)
        self.top_frame.pack(fill="x", padx=10, pady=5)

        # Botón Volver
        self.boton_volver = tk.Button(self.top_frame, text="Volver", command=self.volver_a_limites)
        self.boton_volver.pack(side="left", padx=5)

        self.localidades_frame = tk.Frame(self.frame)
        self.localidades_frame.pack(fill="both", expand=True, padx=10, pady=10)
        


    def defaults(self):
        if self.controller:
            self.controller.cargar_directorios_guardados()
            self.controller.cargar_localidades() 

    def volver_a_limites(self):
        """Vuelve a la vista de límites.""" 
        self.hide()
        self.volver_a_ajustes_callback()

    def hide(self):
        """Oculta esta vista.""" 
        self.frame.pack_forget()

    def show(self):
        """Muestra esta vista.""" 
        self.frame.pack(fill="both", expand=True)
