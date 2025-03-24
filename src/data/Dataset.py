from utils.helpers import load_yaml, check_param

from abc import ABC
import pandas as pd
import pickle
import os

# Clase base abstracta para todos los datasets
class Dataset(ABC):
    def _new_name(self, name: str = None):
        # Genera un nombre único para el dataset
        counter = 0
        base_name = name if name else self.default_name
        while True:
            potential_name = f"{base_name}{'' if counter == 0 else counter}"
            potential_path = os.path.join(self.path, potential_name)
            if not os.path.exists(potential_path):
                self.name = potential_name
                break
            counter += 1
    
    def set_path(self, path: str):
        """Establece una nueva ruta para el dataset"""
        if not isinstance(path, str) or not path:
            raise ValueError("La ruta debe ser una cadena no vacía.")
        if not os.path.exists(path):
            raise NotADirectoryError(f"La ruta especificada no es un directorio válido: {path}")
        self.path = path

    def save(self):
        """Guarda el dataset sempre en format pickle"""
        if self.data is None or self.metadata is None:
            raise ValueError("No se puede guardar un dataset vacío. Asegúrese de que 'data' y 'metadata' no sean None.")
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, 'wb') as f:
            pickle.dump({'data': self.data, 'metadata': self.metadata}, f)

    def export(self, path: str, format: str = 'csv'):
        """Exporta el dataset a un format especificat"""
        if self.data is None or self.metadata is None:
            raise ValueError("No se puede exportar un dataset vacío. Asegúrese de que 'data' y 'metadata' no sean None.")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if format == 'csv' and isinstance(self.data, pd.DataFrame):
            self.data.to_csv(path, index=False)
        else:
            raise ValueError(f"Formato no soportado: {format}")