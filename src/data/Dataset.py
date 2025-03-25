from abc import ABC
import pandas as pd
import pickle
import os

# Clase base abstracta para todos los datasets
class Dataset(ABC):
    # TODO: _new_name & change_name s'haurien de poder unificar (?) en un setter de name
    def _new_name(self, default_name: str = "dataset", name: str = None):
        # Genera un nombre único para el dataset
        counter = 0
        base_name = name if name else default_name
        while True:
            potential_name = f"{base_name}{'' if counter == 0 else counter}"
            potential_path = os.path.join(self.path, potential_name)
            if not os.path.exists(potential_path):
                self.name = potential_name
                break
            counter += 1

    def change_name(self, new_name: str):
        """Cambia el nombre del dataset"""
        if not isinstance(new_name, str) or not new_name:
            raise ValueError("El nombre debe ser una cadena no vacía.")
        self._new_name(new_name)
    
    def set_path(self, path: str):
        """Establece una nueva ruta para el dataset"""
        if not isinstance(path, str) or not path:
            raise ValueError("La ruta debe ser una cadena no vacía.")
        if not os.path.exists(path):
            raise NotADirectoryError(f"La ruta especificada no es un directorio válido: {path}")
        self.path = path

    def metadata(self):
        return {
            "type": self.type,
            "num_particules": self.num_particules,
            "num_passos": self.num_passos
        }

    def data(self):
        return {
            "x": self.x,
            "y": self.y
        }

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