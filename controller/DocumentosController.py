import os
import sys
from tkinter import filedialog, messagebox
import shutil
from components.get_path_images import get_path_images

from fpdf import FPDF
import pandas as pd

class DocumentosController:
    def __init__(self, model, view, volver_a_main_callback):
        self.model = model
        self.view = view
        self.volver_a_main_callback = volver_a_main_callback
        self.view.set_controller(self)

    def get_path(self, filename):
        """Retorna la ruta persistente en 'resources' dentro de AppData."""
        base_dir = os.path.join(os.environ['APPDATA'], "SuralisLab", "resources")
        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, filename)
    
    

    def handle_caja(self):
        """Carga un archivo Excel predeterminado, extrae valores únicos de la columna 'LOCALIDAD'
        y los guarda en un PDF en una ubicación seleccionada por el usuario con una imagen de fondo."""
        file_path = self.get_path("Libro2.xlsx")

        try:
            df = pd.read_excel(file_path)  # Cargar archivo Excel
            if "LOCALIDAD" not in df.columns:
                messagebox.showerror("Error", "La columna 'LOCALIDAD' no existe en el archivo.")
                return

            valores_unicos = df["LOCALIDAD"].drop_duplicates().tolist()

            # Preguntar al usuario dónde guardar el archivo PDF
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
                title="Guardar archivo PDF como"
            )

            if not save_path:
                messagebox.showwarning("Cancelado", "No se seleccionó una ubicación para guardar el archivo.")
                return

            # Crear un archivo PDF
            pdf = FPDF(format='letter')
            pdf.set_auto_page_break(auto=True, margin=15)

            # Agregar una imagen de fondo que ocupe toda la página (tamaño carta)
            ##background_image_path = "images/fondo.jpeg"  # Asegúrate de tener esta imagen

            pdf.set_font("Arial", size=12)
            
            # Agregar la primera página antes de la iteración
            pdf.add_page()
            ##pdf.image(background_image_path, x=0, y=0, w=216, h=279)

            # Variable para el incremento en ln
            #ln_increment = 4.77  # Empezamos con un incremento de 0.2
            # Contar las iteraciones y dividir en páginas de 5 en 5
            for index, valor in enumerate(valores_unicos):
                # Si es un nuevo bloque de 5 iteraciones, agrega una nueva página
                if index % 4 == 0 and index != 0:
                    pdf.add_page()
                    ##pdf.image(background_image_path, x=0, y=0, w=216, h=279)


                size = 28
                sizeln= 10
                # Cambiar tamaño de fuente a 24 para todos los valores
                pdf.set_font("Arial", size=size)  # Cambiar a tamaño 24
                pdf.cell(200, 10, f"PTAS {valor}".upper(), ln=True, align='C')
                pdf.ln(sizeln)

                pdf.set_font("Arial", size=size)
                pdf.cell(200, 10, "LABORATORIO CONTROL PROCESOS", ln=True, align='C')
                pdf.ln(sizeln)

                # Imagen adicional encima del fondo
                image_path = get_path_images("Imagen1.png")
                x_position = pdf.x + 68.5
                y_position = pdf.y - 2.8
                # h = alto y w = ancho
                pdf.image(image_path, x=x_position, y=y_position, w=54, h=24)  # Cambié w y h a 50
                pdf.set_font("Arial", size=12)

                pdf.ln(26)
                # Incrementar el valor de ln para la siguiente iteración
                #pdf.ln(18 + ln_increment)  # Aumentamos el valor de ln en cada iteración

                # Aumentar el incremento para la siguiente imagen
                #ln_increment += 0

                # Mostrar mensaje cuando el índice sea múltiplo de 5
                if (index + 1) % 4 == 0:
                    print(f"Se alcanzó el múltiplo de 4: Iteración {index + 1}, Valor: {valor}")

            pdf.output(save_path)
            messagebox.showinfo("Éxito", f"Archivo PDF guardado en: {save_path}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")



    def handle_muestra(self):
        """Carga un archivo Excel predeterminado, extrae valores únicos de la columna 'LOCALIDAD' y los guarda en un PDF en una ubicación seleccionada por el usuario."""
        file_path = self.get_path("Libro2.xlsx")
            
        try:
            df = pd.read_excel(file_path)  # Cargar archivo Excel
            if "LOCALIDAD" not in df.columns or "PUNTO MUESTREO" not in df.columns:
                messagebox.showerror("Error", "Las columnas requeridas no existen en el archivo.")
                return
            
            # Agrupar los puntos de muestreo por localidad
            localidades = df.groupby("LOCALIDAD")["PUNTO MUESTREO"].apply(list).to_dict()
            
            # Preguntar al usuario dónde guardar el archivo PDF
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
                title="Guardar archivo PDF como"
            )
            
            if not save_path:
                messagebox.showwarning("Cancelado", "No se seleccionó una ubicación para guardar el archivo.")
                return
            
            # Crear un archivo PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            for localidad, puntos in localidades.items():
                pdf.add_page()
                #pdf.set_font("Arial", size=20)
                #pdf.cell(200, 10, f"LOCALIDAD: {localidad}".upper(), ln=True, align='C')
                
                pdf.set_font("Arial", size=14)
                for punto in puntos:
                    pdf.ln(10)
                    pdf.cell(200, 10, f"PTAS {localidad}".upper(), ln=True, align='C')
                    pdf.set_font("Arial", size=14)
                    pdf.cell(200, 10, f"{punto}", ln=True, align='C')  # Reemplaza con el punto de muestreo
                    pdf.set_font("Arial", size=14)
            
            pdf.output(save_path)
            messagebox.showinfo("Éxito", f"Archivo PDF guardado en: {save_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")



    def handle_hoja_ruta(self):
        """Genera un PDF con tablas separadas por localidad, mostrando Puntos de Muestreo, Fecha y Hora con paginación y un espacio para nombre y firma en la última hoja de cada localidad."""
        file_path = self.get_path("Libro2.xlsx")
            
        try:
            df = pd.read_excel(file_path)  # Cargar archivo Excel
            if "LOCALIDAD" not in df.columns or "PUNTO MUESTREO" not in df.columns:
                messagebox.showerror("Error", "Las columnas requeridas no existen en el archivo.")
                return
            
            # Agrupar los puntos de muestreo por localidad
            localidades = df.groupby("LOCALIDAD")["PUNTO MUESTREO"].apply(list).to_dict()
            
            # Preguntar al usuario dónde guardar el archivo PDF
            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
                title="Guardar archivo PDF como"
            )
            
            if not save_path:
                messagebox.showwarning("Cancelado", "No se seleccionó una ubicación para guardar el archivo.")
                return
            
            # Crear el PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)

            max_rows_per_page = 27  # Máximo de filas por página antes de hacer un salto

            for localidad, puntos in localidades.items():
                total_pages = (len(puntos) // max_rows_per_page) + (1 if len(puntos) % max_rows_per_page else 0)
                current_page = 1

                for i in range(0, len(puntos), max_rows_per_page):
                    pdf.add_page()
                    
                    # Número de página en la esquina superior derecha
                    pdf.set_font("Arial", size=10)
                    pdf.cell(0, 10, f"{current_page}/{total_pages}", align='R')
                    pdf.ln(5)

                    # Título de la Localidad
                    pdf.set_font("Arial", size=14, style='B')
                    pdf.cell(200, 10, f"LOCALIDAD: {localidad}".upper(), ln=True, align='C')

                    y = 8

                    # Encabezados de la tabla
                    pdf.set_font("Arial", size=12, style='B')
                    pdf.cell(70, y, "Punto de Muestreo", border=1, align='C')
                    pdf.cell(60, y, "Fecha", border=1, align='C')
                    pdf.cell(60, y, "Hora", border=1, ln=True, align='C')

                    pdf.set_font("Arial", size=10)

                    # Agregar filas de datos (máximo por página)
                    for punto in puntos[i:i + max_rows_per_page]:
                        pdf.cell(70, y, punto, border=1, align='C')
                        pdf.cell(60, y, "", border=1, align='C')  # Celda vacía para Fecha
                        pdf.cell(60, y, "", border=1, ln=True, align='C')  # Celda vacía para Hora

                    # Si es la última página de la localidad, agregar "Nombre y Firma"
                    if current_page == total_pages:
                        # Espacio antes de la firma en la última hoja de cada localidad
                        pdf.ln(10)
                        pdf.set_font("Arial", size=12, style='B')
                        pdf.cell(90, 10, "Nombre: _____________________________________    Firma: ____________________", align='L')
 

                    current_page += 1  # Incrementar contador de páginas para la localidad
                
            pdf.output(save_path)
            messagebox.showinfo("Éxito", f"Archivo PDF guardado en: {save_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")

    def volver_a_main(self):
        """Método para volver a la vista principal."""
        self.volver_a_main_callback()

