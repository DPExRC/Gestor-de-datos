from datetime import datetime, timedelta
import os
import sys
from tkinter import messagebox
import pandas as pd
from openpyxl import load_workbook
import pkg_resources

class ResultadosExcelModel:
    def __init__(self):
        self.headers = []
        self.all_data = []
        self.df = []
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
        """Carga el archivo y agrega la columna 'ÍNDICE'"""
        try:
            # Leer el archivo Excel en un DataFrame
            df = pd.read_excel(file_path)

            # Guardar los encabezados de las columnas
            self.headers = list(df.columns)

            # Convertir los datos del DataFrame a una lista de listas
            self.all_data = df.fillna("").values.tolist()

            # Guardar el DataFrame en un atributo para poder manipularlo más tarde
            self.df = df  # Guardar el DataFrame completo para futuras manipulaciones


            return self.headers, self.all_data 

        except Exception as e:
            self.show_error("Error al cargar el archivo", str(e))
            return [], []


    def show_message(self, title, message):
        """Muestra un mensaje de información."""
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        """Muestra un mensaje de error."""
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        """Muestra un mensaje de advertencia."""
        messagebox.showwarning(title, message)




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
            "miercoles": 2,
            "jueves": 3,
            "viernes": 4,
            "sabado": 5,
            "domingo": 6,
        }

        fechas_reales = []
        for dia in dias:
            dia = dia.strip().lower()

            # Verificar si es un rango de días (ejemplo: viernes-lunes)
            if "-" in dia:
                dia_inicio, dia_fin = dia.split("-")
                dia_inicio = dia_inicio.strip()
                dia_fin = dia_fin.strip()

                if dia_inicio in dias_semana and dia_fin in dias_semana:
                    inicio = dias_semana[dia_inicio]
                    fin = dias_semana[dia_fin]

                    # Si el rango es invertido (viernes-lunes), considerar fin de semana
                    if inicio <= fin:
                        for fecha in fechas_mes:
                            if inicio <= fecha.weekday() <= fin:
                                fechas_reales.append(fecha.strftime("%d/%m/%Y"))
                    else:
                        # Rango invertido: viernes-lunes
                        for fecha in fechas_mes:
                            if fecha.weekday() >= inicio or fecha.weekday() <= fin:
                                fechas_reales.append(fecha.strftime("%d/%m/%Y"))

            else:
                # Día individual
                if dia in dias_semana:
                    for fecha in fechas_mes:
                        if fecha.weekday() == dias_semana[dia]:
                            fechas_reales.append(fecha.strftime("%d/%m/%Y"))

        return fechas_reales

    
    def get_path(self, filename):
        """Retorna la ruta persistente en 'resources' dentro de AppData."""
        base_dir = os.path.join(os.environ['APPDATA'], "SuralisLab", "resources")
        os.makedirs(base_dir, exist_ok=True)
        return os.path.join(base_dir, filename)

    def unidad(self):
        file = self.get_path("Unidades.xlsx")

        try:
            df = pd.read_excel(file)
            return df
        except Exception as e:
            print(e)

    def asignar_unidades(self):
        try:
            df_unidades = self.unidad()
            unidad_idx = self.headers.index("UNIDAD")
            analisis_idx = self.headers.index("ANALISIS")

            for row in self.all_data:
                analisis_lower = str(row[analisis_idx]).strip().lower()
                unidad = df_unidades.loc[
                    df_unidades["ANALISIS"].str.lower() == analisis_lower, "UNIDAD"
                ].values
                if unidad.size > 0:
                    row[unidad_idx] = unidad[0]
        except Exception as e:
            print(f"Error al asignar unidades: {e}")


    def loading_file(self):
        """Cargar datos del archivo Excel seleccionado y procesarlos."""


        file_path = self.get_path("Libro2.xlsx")
        # Leer el archivo sin usar ninguna columna como índice
        df = pd.read_excel(file_path, index_col=None)

        if "DIAS DE MUESTREO" in df.columns:
            df = df.drop(columns=["DIAS DE MUESTREO"])

        if "PROGRAMA" in df.columns:
            expanded_rows = []
            hoy = datetime.now()
            anio, mes = hoy.year, hoy.month

            for _, row in df.iterrows():
                programas = str(row["PROGRAMA"]).split(",")
                programas = [p.strip() for p in programas if p.strip()]
                fechas_reales = self.dias_a_fechas(programas, anio, mes)

                for fecha in fechas_reales:
                    new_row = row.copy()
                    new_row["FECHAS MUESTREO"] = f"{fecha}"
                    expanded_rows.append(new_row)

            df = pd.DataFrame(expanded_rows)
            df = df.drop(columns=["PROGRAMA"], errors="ignore")

        if any(col in df.columns for col in self.analysis_columns.values()):
            df["ANALISIS"] = df[list(self.analysis_columns.values())] \
                .apply(lambda row: ", ".join(row.dropna().astype(str)), axis=1)
            df = df.drop(columns=[col for col in self.analysis_columns.values() if col in df.columns])

            expanded_rows = []
            for _, row in df.iterrows():
                analisis = str(row["ANALISIS"]).split(",")
                analisis = [a.strip() for a in analisis if a.strip()]

                for analisis_item in analisis:
                    new_row = row.copy()
                    new_row["ANALISIS"] = analisis_item
                    expanded_rows.append(new_row)

            df = pd.DataFrame(expanded_rows)

        if "FECHAS MUESTREO" in df.columns:
            idx = df.columns.get_loc("FECHAS MUESTREO") + 1
            df.insert(idx, "FECHA RECEPCION", " ")
            df.insert(idx + 1, "FECHA DIGITACION", " ")
            df.insert(idx + 3, "RESULTADO", " ")
            df.insert(idx + 4, "UNIDAD", " ")

        columns_except_analysis = [col for col in df.columns if col != "ANALISIS"]
        columns_order = columns_except_analysis[:-2] + ["ANALISIS"] + columns_except_analysis[-2:]
        df = df[columns_order]

        self.headers = list(df.columns)
        self.all_data = df.values.tolist()
                    # Asignar unidades automáticamente después de cargar los datos
        self.asignar_unidades()

        return self.headers, self.all_data

    def export_to_excel(self, data, headers, file_path):
        """Exportar los datos a un archivo Excel"""

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

