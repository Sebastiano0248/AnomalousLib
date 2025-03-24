from utils.helpers import load_param, check_param
from data.Dataset import Dataset

from scipy.stats import norm
import numpy as np

# Clase para datos generados
class GeneratedDataset(Dataset):
    def __init__(self, name: str = None, num_particules=None, num_passos=None): # TODO Nom sempre diferent
        self._new_name("generated_dataset", name)
        self.data = None
        self.metadata = {
            "type": "generated",
            "num_particules": check_param("num_particules", num_particules, 100),
            "num_passos": check_param("num_passos", num_passos, 1000)
        }
        self.path = load_param("path", {"dataset_paths", "generated"})

    def generate_random_walk(self, tipus="nonstop"):
        movements = load_param("setting", {"Generated Dataset", "Random Walk", "Nonstop"})
        if tipus == "chill_stop":
            movements = load_param("setting", {"Generated Dataset", "Random Walk", "Chill stop"})
        elif tipus == "hard_stop":
            movements = load_param("setting", {"Generated Dataset", "Random Walk", "Hard stop"})

        for i in range(1, self.num_passos):
            dx = np.zeros(self.num_particules)
            dy = np.zeros(self.num_particules)
            for j in range(self.num_particules):
                dx[j], dy[j] = movements[np.random.randint(0, len(movements))]
            self.data["x"][:, i] = self.data["x"][:, i - 1] + dx
            self.data["y"][:, i] = self.data["y"][:, i - 1] + dy
        return self.metadata, self.data

    def generate_brownian_trajectory(self, tipus="numpy", delta_t=DELTA_T, sigma=SIGMA):
        for i in range(1, self.num_passos):
            if tipus == "numpy":
                dx = np.random.normal(0, sigma * np.sqrt(delta_t), self.num_particules)
                dy = np.random.normal(0, sigma * np.sqrt(delta_t), self.num_particules)
            elif tipus == "scipy":
                dx = norm.rvs(loc=0, scale=sigma * np.sqrt(delta_t), size=self.num_particules)
                dy = norm.rvs(loc=0, scale=sigma * np.sqrt(delta_t), size=self.num_particules)
            self.data["x"][:, i] = self.data["x"][:, i - 1] + dx
            self.data["y"][:, i] = self.data["y"][:, i - 1] + dy
        return self.metadata, self.data

