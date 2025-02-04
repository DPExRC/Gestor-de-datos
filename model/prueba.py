from openpyxl import load_workbook


def delete_rows_in_file(self, file_path, rows_to_delete):
    """
    Elimina las filas especificadas del archivo Excel original.

    Args:
        file_path (str): Ruta del archivo Excel.
        rows_to_delete (list): Lista de índices de fila a eliminar (1-indexados).
            Se recomienda omitir la fila de encabezados (por ejemplo, usar índices >=2).

    Returns:
        bool: True si la operación fue exitosa, False en caso de error.
    """
    try:
        # Cargar el libro de Excel usando openpyxl
        wb = load_workbook(file_path)
        ws = wb.active

        # Ordenar los índices de filas a eliminar en orden descendente para evitar problemas de reindexación
        for row_idx in sorted(rows_to_delete, reverse=True):
            ws.delete_rows(row_idx)

        # Guardar el libro sobrescribiendo el archivo original
        wb.save(file_path)
        wb.close()
        return True
    except Exception as e:
        print(f"Error al eliminar filas en el archivo: {e}")
        return False
