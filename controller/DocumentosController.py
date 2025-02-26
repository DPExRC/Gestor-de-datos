from tkinter import filedialog, messagebox
from components.get_path_resources import get_path_resources
from components.get_path_images import get_path_images

from fpdf import FPDF
import pandas as pd

class DocumentosController:
    def __init__(self, model, view, volver_a_main_callback):
        self.model = model
        self.view = view
        self.volver_a_main_callback = volver_a_main_callback
        self.view.set_controller(self)


    
    def handle_caja(self):
        """Carga un archivo Excel predeterminado, extrae valores únicos de la columna 'LOCALIDAD'
        y los guarda en un PDF en una ubicación seleccionada por el usuario con una imagen de fondo."""
        file_path = get_path_resources("Libro2.xlsx")

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

            pdf.set_font("Arial", size=12)
            
            # Agregar la primera página antes de la iteración
            pdf.add_page()

            # Establecer la posición de inicio para la primera página (7 mm desde la parte superior)
            pdf.set_y(7)

            # Contar las iteraciones y dividir en páginas de 5 en 5
            for index, valor in enumerate(valores_unicos):
                # Si es un nuevo bloque de 3 iteraciones, agrega una nueva página
                if index % 3 == 0 and index != 0:
                    pdf.add_page()
                    # Restablecer la posición en la nueva página
                    pdf.set_y(7)

                size = 31
                size2 = 50
                sizeln = 16

                # Escribir el encabezado "PTAS {valor}"
                pdf.set_font("Arial", "B", size=size2)  
                pdf.cell(200, 10, f"PTAS {valor}".upper(), ln=True, align='C')
                pdf.ln(sizeln)  # Mover hacia abajo

                # Escribir "LABORATORIO CONTROL PROCESOS"
                pdf.set_font("Arial", size=size)
                pdf.cell(200, 10, "LABORATORIO CONTROL PROCESOS", ln=True, align='C')
                pdf.ln(sizeln)  # Mover hacia abajo

                # Imagen adicional encima del fondo
                image_path = get_path_images("Imagen1.png")
                x_position = pdf.x + 55.22
                y_position = pdf.y - 8.8
                # h = alto y w = ancho
                w = 68.37
                h = 21.86
                expand = 1.25
                pdf.image(image_path, x=x_position, y=y_position, w=w*expand, h=h*expand)
                pdf.ln(21)  # Mover hacia abajo después de la imagen

                # Separador de línea que ocupa todo el ancho de la página
                pdf.set_font("Arial", size=10)
                pagina_ancho = 216  # Ancho de la página carta en mm
                margen_izquierdo = 10  # Márgenes izquierdo
                margen_derecho = 10    # Márgenes derecho
                linea_anchura = pagina_ancho - margen_izquierdo - margen_derecho  # Calcular el ancho de la línea
                pdf.cell(linea_anchura, 10, "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------", ln=True)

                # Salto de línea para la siguiente sección
                pdf.ln(4)

                # Mostrar mensaje cuando el índice sea múltiplo de 4
                ##if (index + 1) % 4 == 0:
                ##    print(f"Se alcanzó el múltiplo de 4: Iteración {index + 1}, Valor: {valor}")

            # Guardar el PDF generado
            pdf.output(save_path)
            messagebox.showinfo("Éxito", f"Archivo PDF guardado en: {save_path}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")

    def handle_muestra(self):
        """Carga un archivo Excel predeterminado, extrae valores únicos de la columna 'LOCALIDAD' y los guarda en un PDF en una ubicación seleccionada por el usuario."""
        file_path = get_path_resources("Libro2.xlsx")
            
        try:
            df = pd.read_excel(file_path)  # Cargar archivo Excel
            if "LOCALIDAD" not in df.columns or "MUESTRA" not in df.columns:
                messagebox.showerror("Error", "Las columnas requeridas no existen en el archivo.")
                return
            
            # Agrupar los puntos de muestreo por localidad
            localidades = df.groupby("LOCALIDAD")["MUESTRA"].apply(list).to_dict()
            
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
            ##background_image = get_path_images("fondo2.jpg")  # Ruta de la imagen de fondo

            
            for localidad, puntos in localidades.items():
                pdf.add_page()
                ##pdf.image(background_image, x=0, y=0, w=210, h=297)  # Ajustar imagen a tamaño A4

                pdf.set_y(9)
                #pdf.set_font("Arial", size=20)
                #pdf.cell(200, 10, f"LOCALIDAD: {localidad}".upper(), ln=True, align='C')
                
                pdf.set_font("Arial", size=14)
                for punto in puntos:
                    pdf.set_font("Arial","B", size=22)
                    pdf.cell(200, 10, f"PTAS {localidad}".upper(), ln=True, align='C')
                    pdf.ln(9)

                    pdf.set_font("Arial", size=20)
                    pdf.cell(200, 10, f"{punto}", ln=True, align='C')  # Reemplaza con el punto de muestreo
                    pdf.set_font("Arial", size=14)

                    pdf.set_font("Arial", size=10)
                    pagina_ancho = 216  # Ancho de la página carta en mm
                    margen_izquierdo = 10  # Márgenes izquierdo
                    margen_derecho = 10    # Márgenes derecho
                    linea_anchura = pagina_ancho - margen_izquierdo - margen_derecho  # Calcular el ancho de la línea
                    pdf.cell(linea_anchura, 10, "----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------", ln=True)


            
            pdf.output(save_path)
            messagebox.showinfo("Éxito", f"Archivo PDF guardado en: {save_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")


    def handle_hoja_ruta(self):
        """Genera un PDF con tablas separadas por localidad, mostrando Puntos de Muestreo, Fecha y Hora con paginación y un espacio para nombre y firma en la última hoja de cada localidad."""
        file_path = get_path_resources("Libro2.xlsx")
            
        try:
            df = pd.read_excel(file_path)  # Cargar archivo Excel
            if "LOCALIDAD" not in df.columns or "MUESTRA" not in df.columns:
                messagebox.showerror("Error", "Las columnas requeridas no existen en el archivo.")
                return
            
            # Agrupar los puntos de muestreo por localidad
            localidades = df.groupby("LOCALIDAD")["MUESTRA"].apply(list).to_dict()
            
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
                    pdf.cell(70, y, "Muestra", border=1, align='C')
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

