from datetime import datetime, timedelta
import pandas as pd
from openpyxl import load_workbook
import pkg_resources

class ResultadosExcelModel:
    def __init__(self):
        self.headers = []
        self.all_data = []

        self.is_modified = None 
        self.headermodel = []
        self.all_datamodel = []

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

    def load_file(self, file_path):
        """Cargar datos del archivo Excel seleccionado y procesarlos."""
        df = pd.read_excel(file_path)
        self.original_indices = (df.index + 2).tolist()  # Lista con el número de fila original

        self.excel_data = df
        self.headers = list(df.columns)
        self.all_data = df.values.tolist() 


        return self.headers, self.all_data

    def load_default_file(self):
        """Cargar un archivo predeterminado desde los recursos de la aplicación."""
        try:
            # Usamos pkg_resources para acceder al archivo dentro del paquete
            file_path = pkg_resources.resource_filename(__name__, '../resources/Libro2.xlsx')

            return file_path # self.load_file(file_path)
        except Exception as e:
            print(f"Error al cargar el archivo predeterminado: {e}")
            return [], []  # Retorna vacío si ocurre un error
        
    def loading_default_file(self):
        """Cargar un archivo predeterminado desde los recursos de la aplicación."""
        try:
            # Usamos pkg_resources para acceder al archivo dentro del paquete
            file_path = pkg_resources.resource_filename(__name__, '../resources/Libro2.xlsx')

            return file_path
        except Exception as e:
            print(f"Error al cargar el archivo predeterminado: {e}")
            return [], []  # Retorna vacío si ocurre un error
    
    def obtener_fechas_mes(self, anio, mes):
        """Obtener todas las fechas del mes."""
        primer_dia_mes = datetime(anio, mes, 1)
        if mes == 12:
            ultimo_dia_mes = datetime(anio + 1, 1, 1) - timedelta(days=1)
        else:
            ultimo_dia_mes = datetime(anio, mes + 1, 1) - timedelta(days=1)

        fechas_mes = []
        dia_actual = primer_dia_mes
        while dia_actual <= ultimo_dia_mes:
            fechas_mes.append(dia_actual)
            dia_actual += timedelta(days=1)

        return fechas_mes
    

    def dias_a_fechas(self, dias, anio, mes):
        """Convertir días de la semana (lunes, martes, etc.) a fechas reales del mes."""
        fechas_mes = self.obtener_fechas_mes(anio, mes)
        dias_semana = {
            "lunes": 0,
            "martes": 1,
            "miércoles": 2,
            "jueves": 3,
            "viernes": 4,
            "sábado": 5,
            "domingo": 6,
        }

        fechas_reales = []
        for dia in dias:
            dia = dia.strip().lower()

            # Verificar si es un rango de días (ejemplo: lunes-domingo)
            if "-" in dia:
                dia_inicio, dia_fin = dia.split("-")
                dia_inicio = dia_inicio.strip()
                dia_fin = dia_fin.strip()

                if dia_inicio in dias_semana and dia_fin in dias_semana:
                    # Obtener los índices de los días de la semana
                    inicio = dias_semana[dia_inicio]
                    fin = dias_semana[dia_fin]

                    # Generar todas las fechas entre el inicio y el fin (inclusive)
                    for fecha in fechas_mes:
                        if inicio <= fecha.weekday() <= fin:
                            fechas_reales.append(fecha.strftime("%d/%m/%Y"))
            else:
                # Si no es un rango, procesar como un solo día
                if dia in dias_semana:
                    for fecha in fechas_mes:
                        if fecha.weekday() == dias_semana[dia]:
                            fechas_reales.append(fecha.strftime("%d/%m/%Y"))

        return fechas_reales
    

    def loading_file(self):
        """Cargar datos del archivo Excel seleccionado y procesarlos."""
        # Usamos pkg_resources para acceder al archivo dentro del paquete
        file_path = pkg_resources.resource_filename(__name__, '../resources/Libro2.xlsx')

        df = pd.read_excel(file_path)

        if "DIAS DE MUESTREO" in df.columns:
            df = df.drop(columns=["DIAS DE MUESTREO"])

        # Verificar si la columna "PROGRAMA" existe en el archivo
        if "PROGRAMA" in df.columns:
            expanded_rows = []

            # Obtener el año y mes actual (puedes cambiarlo si es necesario)
            hoy = datetime.now()
            anio = hoy.year
            mes = hoy.month

            for _, row in df.iterrows():
                programas = str(row["PROGRAMA"]).split(",")  # Dividir programas por ","
                programas = [p.strip() for p in programas if p.strip()]  # Limpiar espacios

                # Convertir días de la semana a fechas reales
                fechas_reales = self.dias_a_fechas(programas, anio, mes)

                for fecha in fechas_reales:
                    new_row = row.copy()  # Copiar la fila original
                    new_row["FECHAS MUESTREO"] = f"{fecha} 00:00"  # Asignar la fecha real
                    expanded_rows.append(new_row)

            df = pd.DataFrame(expanded_rows)  # Convertir la lista de filas expandidas a DataFrame

            # Eliminar la columna "PROGRAMA" original si existe
            if "PROGRAMA" in df.columns:
                df = df.drop(columns=["PROGRAMA"])

        # Crear la columna "ANALISIS" a partir de las columnas de análisis
        if any(col in df.columns for col in self.analysis_columns.values()):
            df["ANALISIS"] = df[list(self.analysis_columns.values())] \
                .apply(lambda row: ", ".join(row.dropna().astype(str)), axis=1)
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

            df = pd.DataFrame(expanded_rows)  # Convertir la lista de filas expandidas a DataFrame

        # Insertar columnas "FECHA RECEPCION" y "FECHA DIGITACION" después de "FECHAS DE MUESTREO"
        if "FECHAS MUESTREO" in df.columns:
            idx = df.columns.get_loc("FECHAS MUESTREO") + 1
            df.insert(idx, "FECHA RECEPCION", " ")
            df.insert(idx + 1, "FECHA DIGITACION", " ")
            df.insert(idx + 3, "RESULTADO", " ")
            df.insert(idx + 4, "UNIDAD", " ")

        # Obtener la lista de columnas sin "ANALISIS"
        columns_except_analysis = [col for col in df.columns if col != "ANALISIS"]

        # Asegurar que "ANALISIS" quede en la antepenúltima posición
        columns_order = columns_except_analysis[:-2] + ["ANALISIS"] + columns_except_analysis[-2:]

        df = df[columns_order]

        self.headers = list(df.columns)
        self.all_data = df.values.tolist()
        return self.headers, self.all_data

    def export_to_excel(self, data, headers, file_path):
        """Exportar los datos a un archivo Excel"""

        if not self.is_modified:
            print("No se ha realizado ningún cambio, no es necesario guardar.")
            return
        
        df = pd.DataFrame(data, columns=headers)

        if "ANÁLISIS" in df.columns:
            for key, column in self.analysis_columns.items():
                df[column] = df["ANÁLISIS"].apply(
                    lambda x: next(
                        (val.strip() for val in str(x).split(",") if val.strip().upper() == key), None
                    )
                )
            df = df.drop(columns=["ANÁLISIS"])
        
        if "RESULTADO" in df.columns:
            df["RESULTADO"] = pd.to_numeric(df["RESULTADO"], errors="coerce")

        df.to_excel(file_path, index=False)

        wb = load_workbook(file_path)
        ws = wb.active

        for col in ws.columns:
            max_length = max(len(str(cell.value)) for cell in col if cell.value)
            column_letter = col[0].column_letter
            ws.column_dimensions[column_letter].width = max_length + 2

        wb.save(file_path)


    #def delete_rows_in_file(self, file_path, rows_to_delete):
    #    """
    #    Elimina las filas especificadas del archivo Excel original.
#
    #    Args:
    #        file_path (str): Ruta del archivo Excel.
    #        rows_to_delete (list): Lista de índices de fila a eliminar (1-indexados).
    #            Se recomienda omitir la fila de encabezados (por ejemplo, usar índices >=2).
#
    #    Returns:
    #        bool: True si la operación fue exitosa, False en caso de error.
    #    """
    #    try:
    #        # Cargar el libro de Excel usando openpyxl
    #        wb = load_workbook(file_path)
    #        ws = wb.active
#
    #        # Ordenar los índices de filas a eliminar en orden descendente para evitar problemas de reindexación
    #        for row_idx in sorted(rows_to_delete, reverse=True):
    #            ws.delete_rows(row_idx)
#
    #        # Guardar el libro sobrescribiendo el archivo original
    #        wb.save(file_path)
    #        wb.close()
    #        return True
    #    except Exception as e:
    #        print(f"Error al eliminar filas en el archivo: {e}")
    #        return False
#
#