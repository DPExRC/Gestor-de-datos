import pkg_resources
import pandas as pd

try:
    # Obtener la ruta del archivo usando pkg_resources
    file_path = pkg_resources.resource_filename(__name__, '../resources/Libro2.xlsx')
    df = pd.read_excel(file_path)
    print(df)
    # Mostrar la ruta del archivo
    print(f"Ruta del archivo: {file_path}")
    
    # Intentar abrir el archivo (puedes agregar más código para leer el archivo si es necesario)
    with open(file_path, 'rb') as file:
        print("Archivo abierto correctamente")
        print(file_path)
    
except Exception as e:
    print(f"Error al obtener la ruta o abrir el archivo: {e}")
