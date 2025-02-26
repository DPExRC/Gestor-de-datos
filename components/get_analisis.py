import pandas as pd
from components.get_path_resources import get_path_resources


def obtener_datos_analisis():
    ruta_archivo = get_path_resources("Unidades.xlsx")
    try:
        # Cargar el archivo Excel en un DataFrame
        df = pd.read_excel(ruta_archivo, usecols=["ENCABEZADOS", "ANALISIS"])
        # Crear un diccionario donde ENCABEZADOS es la clave y ANALISIS el valor (como string)
        datos_dict = {}
        for _, row in df.iterrows():
            value = row["ENCABEZADOS"]
            key = row["ANALISIS"]
            
            if pd.notna(key) and pd.notna(value):  # Evitar valores NaN
                if key in datos_dict:
                    datos_dict[key] += f", {value}"  # Concatenar valores con coma
                else:
                    datos_dict[key] = value  # Asignar el primer valor como string
        return datos_dict
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return {}