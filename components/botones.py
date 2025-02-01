import tkinter as tk


class EstiloBoton:
    def __init__(self, ancho=10, alto=1, fuente=("Arial", 10)):
        self.style = {
            "width": ancho,
            "height": alto,
            "font": fuente
        }


class BotonBasePlace:
    def __init__(self, frame=None, texto="Botón", comando=None, rely=0.5, estilo_boton=None, usar_grid=False, grid_config=None):
        """
        Clase base para crear botones con valores predeterminados.
        
        Args:
            frame (tk.Frame): Contenedor donde se mostrará el botón.
            texto (str): Texto del botón. Default: "Botón".
            comando (function): Función a ejecutar al hacer clic. Default: None.
            relx (float): Posición horizontal relativa. Default: 0.5 (usado solo con `place`).
            rely (float): Posición vertical relativa. Default: 0.5 (usado solo con `place`).
            estilo_boton (dict): Diccionario con estilos del botón. Default: None.
            usar_grid (bool): Si se usa `grid` en lugar de `place`. Default: False.
            grid_config (dict): Configuración para `grid` (row, column, padx, pady). Default: None.
        """
        # Si no se pasa un frame, se asigna el valor predeterminado self.button_frame
        self.frame = frame if frame is not None else self.button_frame
        self.texto = texto
        self.comando = comando or self.comando_default
        self.rely = rely
        self.estilo_boton = estilo_boton.style if isinstance(estilo_boton, EstiloBoton) else estilo_boton or EstiloBoton().style
        self.usar_grid = usar_grid
        self.grid_config = grid_config or {"row": 0, "column": 0, "padx": 10}

        self.crear_boton()


    def comando_default(self):
        """Comportamiento por defecto si no se pasa un comando."""
        print(f"Se presionó el botón: {self.texto}")

    def crear_boton(self):
        """Método para crear y posicionar el botón."""
        self.boton = tk.Button(
            self.frame,
            text=self.texto,
            command=self.comando,
            **self.estilo_boton
        )
        if self.usar_grid:
            self.boton.grid(**self.grid_config)
        else:
            self.boton.place(relx=0.5, rely=self.rely, anchor="center")


class BotonBaseGrid:
    def __init__(self, frame, select_file, save_command, reset_command, add_row_command, delete_row_command, export_command, volver):
        """
        Clase para crear un conjunto de botones de acción.

        Args:
            frame (tk.Frame): Contenedor donde se colocarán los botones.
            save_command (function): Función para el botón 'Guardar Cambios'.
            reset_command (function): Función para el botón 'Restablecer Filtros'.
            add_row_command (function): Función para el botón 'Añadir Fila'.
            delete_row_command (function): Función para el botón 'Eliminar Fila'.
            export_command (function): Función para el botón 'Exportar'.
        """
        self.frame = frame
        
        self.select_button = self.crear_boton("Seleccionar Archivo", select_file, 0, 0)
        self.save_button = self.crear_boton("Guardar Cambios", save_command, 0, 2)
        self.reset_button = self.crear_boton("Restablecer Filtros", reset_command, 0, 3)
        self.add_row_button = self.crear_boton("Añadir Fila", add_row_command, 0, 4)
        self.delete_row_button = self.crear_boton("Eliminar Fila", delete_row_command, 0, 5)
        self.export_button = self.crear_boton("Exportar", export_command, 0, 6)
        self.volver_button = self.crear_boton("Volver", volver, 0, 7)

    def crear_boton(self, texto, comando, fila, columna):
        """
        Método para crear un botón.

        Args:
            texto (str): Texto que aparece en el botón.
            comando (function): Función a ejecutar al presionar el botón.
            fila (int): Fila en la que se colocará el botón.
            columna (int): Columna en la que se colocará el botón.
        """
        boton = tk.Button(self.frame, text=texto, command=comando)
        boton.grid(row=fila, column=columna, padx=10)
        return boton
