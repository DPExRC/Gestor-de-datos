class BaseView:
    def __init__(self, root, regresar_view):
        """
        Inicializa la clase base para manejar las vistas.

        Args:
            root (tk.Tk): Ventana principal.
            regresar_view (function): Función para regresar a la vista principal.
        """
        self.root = root
        self.regresar_view = regresar_view
        self.views = {}  # Inicializar un diccionario para guardar referencias a las vistas

    def mostrar_view(self, view_class, view_key):
        """
        Muestra una nueva vista.

        Args:
            view_class (class): Clase de la vista a mostrar.
            view_key (str): Clave para identificar la vista.
        """
        for widget in self.root.winfo_children():
            widget.destroy()  # Limpiar la pantalla actual

        # Crear una instancia de la vista y mostrarla
        view_instance = view_class(self.root, self.regresar_view)
        self.views[view_key] = view_instance  # Guardar la referencia de la vista
