from utils.helpers import load_yaml, check_param
from data.Dataset import Dataset

import pandas as pd
import pickle
import os

# Clase para datos reales descargados
class RealDataset(Dataset):
    def __init__(self, name: str = None): # TODO Nom sempre diferent
        self._new_name("real_dataset", name)
        self.data = None
        self.metadata = {
            "type": "raw",
            "num_particules": check_param("num_particules", num_particules, 100),
            "num_passos": check_param("num_passos", num_passos, 1000)
        }
        self.path = load_yaml("dataset_paths", "raw")

    @classmethod
    def load(cls, path: str):
        """Carga un dataset desde archivo"""
        with open(path, 'rb') as f:
            content = pickle.load(f)
        dataset = cls(name=os.path.basename(path))
        dataset.data = content['data']
        dataset.metadata = content.get('metadata', {})
        return dataset

    @classmethod
    def import_data(cls, path: str, format: str = 'csv'):
        """Importa un dataset desde archivo (sin metadatos)"""
        if format == 'csv':
            data = pd.read_csv(path)
        else:
            raise ValueError(f"Formato no soportado: {format}")
        
        dataset = cls(name=os.path.basename(path))
        dataset.data = data
        dataset.metadata = {}
        return dataset