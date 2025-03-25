from utils.helpers import load_param, check_param
from data.Dataset import Dataset

from scipy.stats import norm
import numpy as np


# Clase para datos generados
class GeneratedDataset(Dataset):
    def __init__(self, name: str = None, num_particules=None, num_passos=None): # TODO Nom sempre diferent
        self.path = load_param("path", "dataset>generated")
        self._new_name("generated_dataset", name)
        self.type = "generated"
        self.num_particules = check_param("num_particules", num_particules, 100)
        self.num_passos = check_param("num_passos", num_passos, 1000)
        self.x = np.zeros((self.num_particules, self.num_passos))
        self.y = np.zeros((self.num_particules, self.num_passos))

    def generate_random_walk(self, tipus="nonstop"):
        movements = load_param("setting", f"generated_dataset>random_walk>{tipus}")
        for i in range(1, self.num_passos):
            dx = np.zeros(self.num_particules)
            dy = np.zeros(self.num_particules)
            for j in range(self.num_particules):
                dx[j], dy[j] = movements[np.random.randint(0, len(movements))]
            self.x[:, i] = self.x[:, i - 1] + dx
            self.y[:, i] = self.y[:, i - 1] + dy
        return self.metadata(), self.data()

    def generate_brownian_trajectory(self, tipus="numpy", delta_t=None, sigma=None):
        # Paràmetres per defecte
        delta_t = delta_t if delta_t else load_param("setting", "generated_dataset>brownian_motion>delta_t")
        sigma = sigma if sigma else load_param("setting", "generated_dataset>brownian_motion>sigma")

        # Generar trajectòria
        for i in range(1, self.num_passos):
            if tipus == "numpy":
                dx = np.random.normal(0, sigma * np.sqrt(delta_t), self.num_particules)
                dy = np.random.normal(0, sigma * np.sqrt(delta_t), self.num_particules)
            elif tipus == "scipy":
                dx = norm.rvs(loc=0, scale=sigma * np.sqrt(delta_t), size=self.num_particules)
                dy = norm.rvs(loc=0, scale=sigma * np.sqrt(delta_t), size=self.num_particules)
            self.x[:, i] = self.x[:, i - 1] + dx
            self.y[:, i] = self.y[:, i - 1] + dy
        return self.metadata(), self.data()

