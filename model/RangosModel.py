from tkinter import filedialog
import pandas as pd


class RangosModel:
    def __init__(self):
        self.headers1 = []
        self.all_data1 = []
        self.headers = []
        self.all_data = []
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
        self.predeterminado()


    def predeterminado(self):
        ruta_archivo = "resources/Rangos.xlsx"

        try:
            # Cargar el archivo Excel en un DataFrame
            df = pd.read_excel(ruta_archivo)

            # Seleccionar solo las columnas relevantes
            df = df[["LOCALIDAD", "PUNTO MUESTREO", "ANALISIS", "MINIMO", "MAXIMO"]]

            # Actualizar headers y all_data
            self.headers = list(df.columns)
            self.all_data = df.values.tolist()
            return self.headers, self.all_data

        except FileNotFoundError:
            print(f"Error: Archivo '{ruta_archivo}' no encontrado.")
            return None, None
        except pd.errors.EmptyDataError:
            print(f"Error: El archivo '{ruta_archivo}' está vacío.")
            return None, None
        except pd.errors.ParserError:
            print(f"Error al parsear el archivo '{ruta_archivo}'.")
            return None, None
        except Exception as e:
            print(f"Error al leer el archivo '{ruta_archivo}': {e}")
            return None, None


    def obtener_datos(self):
        ruta_archivo = "resources/Libro2.xlsx"

        try:
            # Cargar el archivo Excel en un DataFrame
            df = pd.read_excel(ruta_archivo)

            # Verificar columnas requeridas
            if "LOCALIDAD" not in df.columns or "PUNTO MUESTREO" not in df.columns:
                raise ValueError("El archivo debe contener las columnas 'LOCALIDAD' y 'PUNTO MUESTREO'.")

            # Crear la columna "ANALISIS" a partir de las columnas de análisis
            analysis_cols = [col for col in self.analysis_columns.values() if col in df.columns]
            if analysis_cols:
                df["ANALISIS"] = df[analysis_cols].apply(
                    lambda row: ", ".join(row.dropna().astype(str)), axis=1
                )
                df = df.drop(columns=analysis_cols)

                # Expandir filas para cada análisis
                expanded_rows = []
                for _, row in df.iterrows():
                    analisis = str(row["ANALISIS"]).split(",")
                    analisis = [a.strip() for a in analisis if a.strip()]  # Limpiar espacios

                    for analisis_item in analisis:
                        new_row = row.copy()
                        new_row["ANALISIS"] = analisis_item
                        expanded_rows.append(new_row)

                df = pd.DataFrame(expanded_rows)

            # Añadir columnas "MÍNIMO" y "MÁXIMO" con valores vacíos
            df["MINIMO"] = ""
            df["MAXIMO"] = ""

            # Seleccionar solo las columnas relevantes
            df = df[["LOCALIDAD", "PUNTO MUESTREO", "ANALISIS", "MINIMO", "MAXIMO"]]

            # Retornar los encabezados y los datos en formato de lista
            self.headers1 = list(df.columns)
            self.all_data1 = df.values.tolist()
            return self.headers1, self.all_data1

        except FileNotFoundError:
            print(f"Error: Archivo '{ruta_archivo}' no encontrado.")
            return None, None
        except pd.errors.EmptyDataError:
            print(f"Error: El archivo '{ruta_archivo}' está vacío.")
            return None, None
        except pd.errors.ParserError:
            print(f"Error al parsear el archivo '{ruta_archivo}'.")
            return None, None
        except Exception as e:
            print(f"Error al leer el archivo '{ruta_archivo}': {e}")
            return None, None

        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo '{ruta_archivo}' no encontrado.")
        except pd.errors.EmptyDataError:
            raise ValueError(f"El archivo '{ruta_archivo}' está vacío.")
        except pd.errors.ParserError:
            raise ValueError(f"Error al parsear el archivo '{ruta_archivo}'.")
        except Exception as e:
            raise RuntimeError(f"Error al leer el archivo '{ruta_archivo}': {e}")
        
