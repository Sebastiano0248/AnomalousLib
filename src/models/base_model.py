from abc import ABC, abstractmethod
import pickle

# Clase base para modelos
class Model(ABC):
    def __init__(self):
        self.trained = False
        self.model = None
    
    @abstractmethod
    def train(self, data, *args, **kwargs):
        pass
    
    @abstractmethod
    def predict(self, data, *args, **kwargs):
        pass
    
    def save_model(self, path: str):
        """Guarda el modelo entrenado"""
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)
    
    def load_model(self, path: str):
        """Carga un modelo pre-entrenado"""
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
        self.trained = True