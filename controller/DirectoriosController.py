import os
import sys
from tkinter import filedialog, messagebox
import openpyxl
import tkinter as tk
from tkinter import ttk

class DirectoriosController:
    def __init__(self, model, view, volver_a_main_callback):
        self.model = model
        self.view = view
        self.volver_a_main_callback = volver_a_main_callback
        self.directorios_dict = {}
        self.localidades = []  # Inicializar lista de localidades
        self.view.set_controller(self)

    def leer_archivo_excel(self, ruta_archivo):
        """Lee un archivo .xlsx y devuelve el contenido de las celdas de la primera columna, comenzando desde la segunda fila."""
        try:
            workbook = openpyxl.load_workbook(ruta_archivo)
            sheet = workbook.active  

            localidades = []

            for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1, values_only=True):
                localidad = row[0]
                if localidad:
                    localidades.append(localidad)

            return localidades
        except FileNotFoundError:
            print(f"El archivo {ruta_archivo} no fue encontrado.")
            return []
        except Exception as e:
            print(f"Error al leer el archivo Excel: {e}")
            return []

    def seleccionar_archivo(self, localidad, label_archivo):
        """Abre un diálogo para seleccionar un archivo .xlsx, lo muestra en la etiqueta y lo guarda en un archivo .txt."""
        archivo = filedialog.askopenfilename(
            title=f"Seleccionar archivo .xlsx para {localidad}",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )
        if archivo:
            label_archivo.config(text=archivo)  # Mostrar la ruta del archivo en la etiqueta
            self.directorios_dict[localidad] = archivo  # Guardar en el diccionario
            self.guardar_directorios()  # Guardar en el archivo .txt

    def get_path(self, filename):
        """Retorna la ruta persistente en 'resources' dentro de AppData."""
        base_dir = os.path.join(os.environ['APPDATA'], "SuralisLab", "resources")
        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, filename)

    def guardar_directorios(self):
        """Guarda las localidades únicas con sus rutas."""
        ruta_guardado = self.get_path("DirectoriosLocalidades.txt")

        try:
            localidades_unicas = set(self.localidades)  # Asegurar que solo haya una coincidencia por localidad

            with open(ruta_guardado, "w", encoding="utf-8") as file:
                for localidad in localidades_unicas:
                    ruta = self.directorios_dict.get(localidad, "Sin asignar")
                    file.write(f"{localidad}: {ruta}\n")

                messagebox.showinfo("Información", "Directorios guardados correctamente.")
        except Exception as e:
            print(f"Error al guardar los directorios: {e}")

    def cargar_localidades(self):
        """Carga las localidades, elimina las repetidas y las muestra en la tabla con un botón de selección de archivo."""
        file_path = self.get_path("Libro2.xlsx")
        self.localidades = list(set(self.leer_archivo_excel(file_path)))  # Eliminar duplicados al cargar
        self.localidades.sort()  # Ordenar alfabéticamente para mayor claridad
        print(self.localidades)

        # Limpiar el frame antes de crear la tabla (solo si es necesario)
        if hasattr(self, 'tree'):
            self.tree.delete(*self.tree.get_children())  # Limpiar solo los datos de la tabla, no destruirla
        else:
            # Si la tabla no existe, crear el contenedor y la tabla
            self.table_container = tk.Frame(self.view.localidades_frame)
            self.table_container.pack(fill="both", expand=True)

            # Crear la tabla para mostrar datos
            self.tree = ttk.Treeview(self.table_container, columns=("Localidad", "Ruta"), show="headings", selectmode='extended')
            # Establecer el estilo en negrita para los encabezados
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("TkDefaultFont", 10, "bold"))

            # Configurar encabezados
            self.tree.heading("Localidad", text="LOCALIDAD")
            self.tree.heading("Ruta", text="RUTA")

            # Ajustar el tamaño horizontal de las columnas
            self.tree.column("Localidad", width=5, anchor="w")  # 200 píxeles, alineado a la izquierda
            self.tree.column("Ruta", width=600, anchor="w")       # 300 píxeles, alineado a la izquierda

            self.tree.bind("<Double-1>", self.start_edit)

            # Empaquetar la tabla después de configurarla
            self.tree.pack(side="left", fill="both", expand=True)

        # Llenar la tabla con los datos de las localidades
        for localidad in self.localidades:
            ruta = self.directorios_dict.get(localidad, "Sin asignar")
            self.tree.insert("", "end", values=(localidad, ruta))

    def start_edit(self, event):
        """Detecta el doble clic en la columna 'Ruta' y abre un seleccionador de archivos."""
        # Obtener la fila y la columna donde se hizo doble clic
        item = self.tree.selection()
        column = self.tree.identify_column(event.x)
        
        # Obtener el valor de la localidad (columna 1) para esa fila
        localidad = self.tree.item(item, 'values')[0]

        if column == "#2":  # Verifica si es la columna "Ruta" (columna 2)
            # Abrir el cuadro de diálogo para seleccionar un archivo, con el título de la localidad
            file_path = tk.filedialog.askopenfilename(title=f"Seleccionar archivo para {localidad}", filetypes=[("Archivos Excel", "*.xls;*.xlsx")])
            
            if file_path:  # Si se seleccionó un archivo
                # Obtener los datos actuales de la fila
                current_values = self.tree.item(item, 'values')
                self.directorios_dict[localidad] = file_path  # Guardar en el diccionario
                self.guardar_directorios()  # Guardar en el archivo .txt
                
                # Actualizar la columna "Ruta" con la nueva ruta seleccionada
                self.tree.item(item, values=(current_values[0], file_path))
                

    def cargar_directorios_guardados(self):
        """Carga las localidades con sus archivos si existen."""
        ruta_guardado = self.get_path("DirectoriosLocalidades.txt")

        try:
            with open(ruta_guardado, "r", encoding="utf-8") as file:
                for linea in file:
                    partes = linea.strip().split(": ", 1)
                    if len(partes) == 2:
                        localidad, ruta = partes
                        self.directorios_dict[localidad] = ruta  # Asignar la ruta al diccionario
        except FileNotFoundError:
            print("No se encontró el archivo de directorios, se iniciará vacío.")
        except Exception as e:
            print(f"Error al cargar los directorios: {e}")
