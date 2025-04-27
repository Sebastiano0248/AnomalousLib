from scipy.stats import levy_stable, pareto
from fbm import FBM
import pandas as pd
import numpy as np

class DatasetGenerator:
    def __init__(self, num_particules):
        self.num_particules = num_particules

    def changeParams(self, num_particules=None):
        # Canvia els paràmetres del generador de dades si es proporcionen nous valors
        if num_particules is not None:
            self.num_particules = num_particules

    def _format_data(self, x, y, trajectory_type, attributes, num_passos):
        # Dona format a les dades generades per a les trajectòries
        data = []
        for i in range(self.num_particules):
            coords = [x[i, :].tolist(), y[i, :].tolist()]
            trajectory_data = {
                "coords": coords,
                "num_steps": num_passos,
                "trajectory_type": trajectory_type,
                "attributes": {k: (v[i] if isinstance(v, list) and len(v) == self.num_particules else v) for k, v in attributes.items()}
            }
            data.append(trajectory_data)
        return pd.DataFrame(data)

    def generate_RandomWalk(self, tipus="nonstop", random_params=False, num_passos=100):
        def _chooseMovementsRandomWalk(tipus):
            # Selecciona els moviments possibles per al camí aleatori segons el tipus especificat
            match tipus:
                case "nonstop": return [[1, 0], [-1, 0], [0, 1], [0, -1]]
                case "chill_stop": return [[1, 0], [-1, 0], [0, 1], [0, -1], [0, 0]]
                case "hard_stop": return [[1, 0], [-1, 0], [0, 1], [0, -1], [0, 0], [0, 0], [0, 0], [0, 0]]
                case _: raise ValueError(f"Unknown movement type: {tipus}")

        x = np.zeros((self.num_particules, num_passos))
        y = np.zeros((self.num_particules, num_passos))

        if random_params:
            tipus_per_particle = np.random.choice(["nonstop", "chill_stop", "hard_stop"], self.num_particules)
        else:
            tipus_per_particle = [tipus] * self.num_particules

        for i in range(1, num_passos):
            dx = np.zeros(self.num_particules)
            dy = np.zeros(self.num_particules)
            for j in range(self.num_particules):
                movements = _chooseMovementsRandomWalk(tipus_per_particle[j])
                dx[j], dy[j] = movements[np.random.randint(0, len(movements))]
            x[:, i] = x[:, i - 1] + dx
            y[:, i] = y[:, i - 1] + dy

        return self._format_data(x, y, "Random Walk", {"movement_type": tipus_per_particle}, num_passos)

    def generate_BrownianMotion(self, generator_type="numpy", delta_t=1, sigma=1, random_params=False, num_passos=100):
        if random_params:
            delta_t_per_particle = np.random.uniform(0.1, 5.0, self.num_particules)
            sigma_per_particle = np.random.uniform(0.1, 3.0, self.num_particules)
        else:
            delta_t_per_particle = [delta_t] * self.num_particules
            sigma_per_particle = [sigma] * self.num_particules

        x = np.zeros((self.num_particules, num_passos))
        y = np.zeros((self.num_particules, num_passos))

        for i in range(1, num_passos):
            for p in range(self.num_particules):
                scale = sigma_per_particle[p] * np.sqrt(delta_t_per_particle[p])
                dx = np.random.normal(0, scale)
                dy = np.random.normal(0, scale)
                x[p, i] = x[p, i - 1] + dx
                y[p, i] = y[p, i - 1] + dy

        return self._format_data(x, y, "Brownian Motion", {"generator_type": generator_type, "delta_t": delta_t_per_particle.tolist(), "sigma": sigma_per_particle.tolist()}, num_passos)
    
    def generate_FractionalBrownianMotion(self, hurst=0.75, random_params=False, num_passos=100):
        if random_params:
            hurst_per_particle = np.random.uniform(0.1, 0.9, self.num_particules)
        else:
            hurst_per_particle = [hurst] * self.num_particules

        x = np.zeros((self.num_particules, num_passos))
        y = np.zeros((self.num_particules, num_passos))

        for p in range(self.num_particules):
            fbm_x = FBM(n=num_passos - 1, hurst=hurst_per_particle[p]).fbm()
            fbm_y = FBM(n=num_passos - 1, hurst=hurst_per_particle[p]).fbm()
            x[p, :] = fbm_x
            y[p, :] = fbm_y

        return self._format_data(x, y, "Fractional Brownian Motion", {"hurst": hurst_per_particle.tolist()}, num_passos)

    def generate_ContinuousTimeRandomWalk(self, alpha=1.2, random_params=False, num_passos=100):
        if random_params:
            alpha_per_particle = np.random.uniform(1.1, 2.5, self.num_particules)
        else:
            alpha_per_particle = [alpha] * self.num_particules

        x = np.zeros((self.num_particules, num_passos))
        y = np.zeros((self.num_particules, num_passos))

        for p in range(self.num_particules):
            wait_times = pareto.rvs(alpha_per_particle[p], size=num_passos)
            times = np.cumsum(wait_times)
            t_norm = np.linspace(0, times[-1], num_passos)
            x[p, :] = np.interp(t_norm, times, np.cumsum(np.random.randn(len(times))))
            y[p, :] = np.interp(t_norm, times, np.cumsum(np.random.randn(len(times))))

        return self._format_data(x, y, "CTRW", {"alpha": alpha_per_particle.tolist()}, num_passos)

    def generate_LevyWalks(self, alpha=1.8, speed=1.0, beta=0.0, random_params=False, num_passos=100):
        if random_params:
            alpha_per_particle = np.clip(np.random.uniform(1.1, 2.0, self.num_particules), 1.1, 2.0)
            beta_per_particle = np.random.uniform(-1.0, 1.0, self.num_particules)
            speed_per_particle = np.random.uniform(0.1, 5.0, self.num_particules)
        else:
            alpha_per_particle = [alpha] * self.num_particules
            beta_per_particle = [beta] * self.num_particules
            speed_per_particle = [speed] * self.num_particules

        x = np.zeros((self.num_particules, num_passos))
        y = np.zeros((self.num_particules, num_passos))

        for p in range(self.num_particules):
            steps = levy_stable.rvs(alpha_per_particle[p], beta_per_particle[p], size=num_passos)
            angles = np.random.uniform(0, 2 * np.pi, num_passos)
            dx = speed_per_particle[p] * np.abs(steps) * np.cos(angles)
            dy = speed_per_particle[p] * np.abs(steps) * np.sin(angles)
            x[p, :] = np.cumsum(dx)
            y[p, :] = np.cumsum(dy)

        return self._format_data(x, y, "Lévy Walk", {"alpha": alpha_per_particle.tolist(), "speed": speed_per_particle.tolist()}, num_passos)

    def generate_AnnealedTransitTimeModel(self, gamma_shape=1.5, random_params=False, num_passos=100):
        if random_params:
            gamma_shape_per_particle = np.random.uniform(0.5, 5.0, self.num_particules)
        else:
            gamma_shape_per_particle = [gamma_shape] * self.num_particules

        x = np.zeros((self.num_particules, num_passos))
        y = np.zeros((self.num_particules, num_passos))

        for p in range(self.num_particules):
            Ds = np.random.gamma(gamma_shape_per_particle[p], size=num_passos)
            dx = np.random.normal(0, np.sqrt(Ds))
            dy = np.random.normal(0, np.sqrt(Ds))
            x[p, :] = np.cumsum(dx)
            y[p, :] = np.cumsum(dy)

        return self._format_data(x, y, "ATTM", {"gamma_shape": gamma_shape_per_particle.tolist()}, num_passos)

    def generate_ScaledBrownianMotion(self, beta=1.3, random_params=False, num_passos=100):
        if random_params:
            beta_per_particle = np.random.uniform(0.5, 2.0, self.num_particules)
        else:
            beta_per_particle = [beta] * self.num_particules

        x = np.zeros((self.num_particules, num_passos))
        y = np.zeros((self.num_particules, num_passos))

        for p in range(self.num_particules):
            t = np.arange(num_passos)
            D_t = (t + 1) ** (beta_per_particle[p] - 1)
            dx = np.random.normal(0, np.sqrt(D_t))
            dy = np.random.normal(0, np.sqrt(D_t))
            x[p, :] = np.cumsum(dx)
            y[p, :] = np.cumsum(dy)

        return self._format_data(x, y, "Scaled Brownian Motion", {"beta": beta_per_particle.tolist()}, num_passos)
