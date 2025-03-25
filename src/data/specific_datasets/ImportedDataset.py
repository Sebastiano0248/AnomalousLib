from utils.helpers import load_param, check_param
from data.Dataset import Dataset

import pandas as pd
import numpy as np
import pickle
import os


# Clase para datos reales descargados
class ImportedDataset(Dataset):
    def __init__(self, name: str = None, num_particules=None, num_passos=None): # TODO Nom sempre diferent
        self.path = load_param("path", "dataset>raw")
        self._new_name("real_dataset", name)
        self.type = "raw"
        self.num_particules = check_param("num_particules", num_particules, 100)
        self.num_passos = check_param("num_passos", num_passos, 1000)
        self.x = np.zeros((self.num_particules, self.num_passos))
        self.y = np.zeros((self.num_particules, self.num_passos))

    @classmethod
    def load(cls, path: str):
        """Carga un dataset desde archivo"""
        with open(path, 'rb') as f:
            content = pickle.load(f)
        dataset = cls(name=os.path.basename(path))
        dataset.x = content['data']['x']
        dataset.y = content['data']['y']
        dataset.type = content['metadata'].get('type', dataset.type)
        dataset.num_particules = content['metadata'].get('num_particules', dataset.num_particules)
        dataset.num_passos = content['metadata'].get('num_passos', dataset.num_passos)
        return dataset

    @classmethod
    def import_data(cls, path: str, format: str = 'csv'):
        """Importa un dataset desde archivo (sin metadatos)"""
        if format == 'csv':
            data = pd.read_csv(path)
            x = data.iloc[:, :-1].to_numpy()
            y = data.iloc[:, -1].to_numpy()
        else:
            raise ValueError(f"Formato no soportado: {format}")
        
        dataset = cls(name=os.path.basename(path))
        dataset.x = x
        dataset.y = y
        return dataset