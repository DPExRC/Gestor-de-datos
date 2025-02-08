import os
from tkinter import filedialog, messagebox
import shutil

from fpdf import FPDF
import pandas as pd

class DocumentosController:
    def __init__(self, model, view, volver_a_main_callback):
        self.model = model
        self.view = view
        self.volver_a_main_callback = volver_a_main_callback
        self.view.set_controller(self)

    def handle_caja(self):
        """Carga un archivo Excel predeterminado, extrae valores únicos de la columna 'LOCALIDAD' y los guarda en un PDF en una ubicación seleccionada por el usuario."""
        file_path = "resources/Libro2.xlsx"
        
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
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", size=20)
            pdf.cell(200, 10, "ETIQUETAS CAJA CONTROL PROCESO", ln=True, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", size=12)
            for valor in valores_unicos:

                #pdf.set_fill_color(200, 200, 200)
                #pdf.rect(10, pdf.y+5, 180, 50, 'D')
                pdf.ln(10)
                pdf.cell(200, 10, f"PTAS {valor}".upper(), ln=True, align='C')


                pdf.set_font("Arial", size=10)
                pdf.cell(200, 10, "LABORATORIO CONTROL PROCESOS", ln=True, align='C')

                pdf.set_font("Arial", size=12)
                pdf.ln(5)

                try:
                    # Ajusta la ruta y las dimensiones según tu necesidad
                    image_path = "images/Imagen1.png"  # Reemplaza con la ruta real de tu imagen
                    x_position = pdf.x + 87  # Posición horizontal (ajusta según tu diseño)
                    y_position = pdf.y - 5  # Posición vertical (debajo del texto anterior + un pequeño espacio)
                    width = 25  # Ancho de la imagen (ajusta según tu necesidad)
                    height = 0  # Altura de la imagen (0 para mantener la relación de aspecto original)

                    pdf.image(image_path, x=x_position, y=y_position, w=width, h=height)

                except Exception as e:
                    print(f"Error al insertar la imagen: {e}")

            pdf.output(save_path)
            messagebox.showinfo("Éxito", f"Archivo PDF guardado en: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")


    def handle_muestra(self):
            """Lógica para el botón 'Caja': Guardar un archivo en una ubicación seleccionada."""
            # Ruta del archivo cargado en el proyecto
            file_path = "resources/etiqueta_botella.pdf"  # Cambia esta ruta por la de tu archivo original

            if os.path.exists(file_path):
                # Mostrar cuadro de diálogo para seleccionar ubicación de guardado
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",  # Extensión predeterminada
                    filetypes=[("Archivos pdf", "*.pdf"), ("Todos los archivos", "*.*")],
                    title="Guardar archivo como"
                )

                if save_path:  # Si el usuario seleccionó una ubicación
                    try:
                        shutil.copy(file_path, save_path)  # Copiar el archivo a la ubicación seleccionada
                        messagebox.showinfo("Éxito", f"Archivo guardado en: {save_path}")
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
                else:
                    messagebox.showwarning("Cancelado", "La operación fue cancelada.")
            else:
                messagebox.showerror("Error", f"El archivo '{file_path}' no existe.")

    def handle_hoja_ruta(self):
            """Lógica para el botón 'Caja': Guardar un archivo en una ubicación seleccionada."""
            # Ruta del archivo cargado en el proyecto
            file_path = "resources/hoja_ruta.pdf"  # Cambia esta ruta por la de tu archivo original

            if os.path.exists(file_path):
                # Mostrar cuadro de diálogo para seleccionar ubicación de guardado
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",  # Extensión predeterminada
                    filetypes=[("Archivos pdf", "*.pdf"), ("Todos los archivos", "*.*")],
                    title="Guardar archivo como"
                )

                if save_path:  # Si el usuario seleccionó una ubicación
                    try:
                        shutil.copy(file_path, save_path)  # Copiar el archivo a la ubicación seleccionada
                        messagebox.showinfo("Éxito", f"Archivo guardado en: {save_path}")
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")
                else:
                    messagebox.showwarning("Cancelado", "La operación fue cancelada.")
            else:
                messagebox.showerror("Error", f"El archivo '{file_path}' no existe.")

    def volver_a_main(self):
        """Método para volver a la vista principal."""
        self.volver_a_main_callback()

