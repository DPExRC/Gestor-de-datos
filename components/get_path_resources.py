import os 

def get_path_resources(filename):
    """Retorna la ruta persistente en 'resources' dentro de AppData."""
    base_dir = os.path.join(os.environ['APPDATA'], "SuralisLab", "resources")
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, filename)