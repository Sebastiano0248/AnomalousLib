from pathlib import Path
import yaml
    
def load_param(paramType: str, *keys):
    yaml_path = Path(f"config/{paramType}s.yaml")
    if not yaml_path.exists():
        raise FileNotFoundError(f"El archivo {yaml_path} no existe.")

    try:
        with yaml_path.open('r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ValueError(f"Error al cargar el archivo YAML: {e}")

    # Navegar por las claves proporcionadas
    for key in keys:
        if not isinstance(data, dict):
            raise ValueError("El dato no es un diccionario, no se puede seguir navegando.")
        data = data.get(key)

    return data

def check_param(param_name, param_value, default_value):
    import warnings
    if param_value is None:
        warnings.warn(f"El parámetro '{param_name}' no ha sido especificado. Usando valor por defecto {default_value}.", UserWarning)
        return default_value
    return param_value