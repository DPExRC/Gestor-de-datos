import pandas as pd
from components.get_path_resources import get_path_resources


class UnidadesModel:
    def __init__(self):
        self.headers1 = []
        self.all_data1 = []
        self.headers = []
        self.all_data = []


    def predeterminado(self):
        ruta_archivo = get_path_resources("Unidades.xlsx")

        try:
            # Cargar el archivo Excel en un DataFrame
            df = pd.read_excel(ruta_archivo)

            # Seleccionar solo las columnas relevantes
            df = df[["ENCABEZADOS", "ANALISIS", "UNIDAD"]]

            # Actualizar headers y all_data
            self.headers = list(df.columns)
            self.all_data = df.values.tolist()
            
            return self.headers, self.all_data
        
        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
            return [], []



    def obtener_datos1(self):
        ruta_archivo = get_path_resources("Libro2.xlsx")

        try:
            # Cargar el archivo Excel en un DataFrame
            df = pd.read_excel(ruta_archivo)


        except Exception as e:
            print(f"Error al procesar el archivo: {e}")
            return [], []

    #def obtener_datos(self):
    #    ruta_archivo = get_path_resources("Libro2.xlsx")
    #    ruta_salida = get_path_resources("Unidades.xlsx")
#
    #    try:
    #        # Cargar el archivo Excel en un DataFrame
    #        df = pd.read_excel(ruta_archivo)
#
    #        # Excluir columnas específicas
    #        columnas_excluir = {"LOCALIDAD", "PROGRAMA", "DIAS DE MUESTRA", "MUESTRA"}
    #        columnas_filtradas = [col for col in df.columns if col not in columnas_excluir]
#
    #        # Lista para almacenar filas expandidas
    #        expanded_rows = []
    #        valores_unicos = set()  # Para evitar duplicados globales en ANÁLISIS
#
    #        for col in columnas_filtradas:
    #            for valor in df[col].dropna():
    #                for item in str(valor).split(","):
    #                    item = item.strip()
    #                    clave = col  # Se mantiene el encabezado original
#
    #                    if item and (clave, item) not in valores_unicos:
    #                        valores_unicos.add((clave, item))
    #                        expanded_rows.append({
    #                            "ENCABEZADOS": clave,
    #                            "ANALISIS": item,
    #                            "UNIDAD": ""
    #                        })
#
    #        # Crear DataFrame y guardar en Excel
    #        df_resultado = pd.DataFrame(expanded_rows)
    #        df_resultado.to_excel(ruta_salida, index=False)
#
    #        # Retornar encabezados y datos para la vista
    #        self.headers1 = df_resultado.columns.tolist()
    #        self.all_data1 = df_resultado.values.tolist()
    #        return self.headers1, self.all_data1
#
    #    except Exception as e:
    #        print(f"Error al procesar el archivo: {e}")
    #        return [], []

