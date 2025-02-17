import os
import shutil

def get_path_images(filename):
    """Retorna la ruta persistente en 'images' dentro de AppData."""
    base_dir = os.path.join(os.environ['APPDATA'], "SuralisLab", "images")
    os.makedirs(base_dir, exist_ok=True)
    
    file_path = os.path.join(base_dir, filename)

    # Si el archivo no existe, copiarlo desde el directorio original del ejecutable
    if not os.path.exists(file_path):
        temp_images_dir = os.path.join(os.path.dirname(__file__), "images")
        original_file = os.path.join(temp_images_dir, filename)

        if os.path.exists(original_file):
            shutil.copy(original_file, file_path)

    return file_path
