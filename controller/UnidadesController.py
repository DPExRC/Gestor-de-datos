import pandas as pd

class UnidadesController:
    def __init__(self):
        self.analysis_columns = {
            "DQO": "DQO",
            "ST": "ST",
            "SST": "SST",
            "SSV": "SSV",
            "PH": "ph",
            "AGV": "AGV (ácido acético)",
            "ALC": "alcalinidad (CaCO3)",
            "HUM": "% humedad",
            "TRAN": "transmitancia",
        }

    def obtener_datos(self):
        ruta_archivo = "resources/Libro2.xlsx"

        try:
            # Cargar el archivo Excel en un DataFrame
            df = pd.read_excel(ruta_archivo)

            # Crear la columna "ANALISIS" a partir de las columnas de análisis
            if any(col in df.columns for col in self.analysis_columns.values()):
                df["ANALISIS"] = df[list(self.analysis_columns.values())] \
                    .apply(lambda row: ", ".join(row.dropna().astype(str)), axis=1)
                
                # Eliminar las columnas originales de análisis
                df = df.drop(columns=[col for col in self.analysis_columns.values() if col in df.columns])

                # Separar los análisis por comas y crear filas adicionales
                expanded_rows = []

                for _, row in df.iterrows():
                    # Obtener los análisis separados por comas
                    analisis = str(row["ANALISIS"]).split(",")
                    analisis = [a.strip() for a in analisis if a.strip()]  # Limpiar espacios

                    # Crear una fila para cada análisis
                    for analisis_item in analisis:
                        new_row = row.copy()  # Copiar la fila original
                        new_row["ANALISIS"] = analisis_item  # Asignar el análisis específico
                        expanded_rows.append(new_row)

                # Convertir la lista de filas expandidas a un DataFrame
                df = pd.DataFrame(expanded_rows)

            # Devolver un DataFrame con las columnas 'LOCALIDAD' y las columnas de análisis
            return df[["ANALISIS"]]
                      
        except FileNotFoundError:
            print(f"Error: Archivo '{ruta_archivo}' no encontrado.")
            return None
        except pd.errors.EmptyDataError:
            print(f"Error: El archivo '{ruta_archivo}' está vacío.")
            return None
        except pd.errors.ParserError:
            print(f"Error al parsear el archivo '{ruta_archivo}'.")
            return None
        except Exception as e:
            print(f"Error al leer el archivo '{ruta_archivo}': {e}")
            return None
