import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from scipy.stats import norm
from config import NUM_PARTICULES, NUM_PASSOS, DELTA_T, SIGMA, T_INICIAL, T_FINAL

class TrajectoryGenerator:
    def __init__(self, method="numpy", num_particules=NUM_PARTICULES, num_passos=NUM_PASSOS, delta_t=DELTA_T, sigma=SIGMA, t_inicial=T_INICIAL, t_final=T_FINAL):
        self.method = method
        self.num_particules = num_particules
        self.num_passos = num_passos
        self.delta_t = delta_t
        self.sigma = sigma
        self.t_inicial = t_inicial
        self.t_final = t_final
        self.x = np.zeros((num_particules, num_passos))
        self.y = np.zeros((num_particules, num_passos))
        self.temps = np.linspace(t_inicial, t_final, num_passos)
        self._generate_trajectories()

    def _generate_trajectories(self):
        for i in range(1, self.num_passos):
            if self.method == "numpy":
                dx = np.random.normal(0, self.sigma * np.sqrt(self.delta_t), self.num_particules)
                dy = np.random.normal(0, self.sigma * np.sqrt(self.delta_t), self.num_particules)
            elif self.method == "scipy":
                dx = norm.rvs(loc=0, scale=self.sigma * np.sqrt(self.delta_t), size=self.num_particules)
                dy = norm.rvs(loc=0, scale=self.sigma * np.sqrt(self.delta_t), size=self.num_particules)
            else:
                raise ValueError("Mètode no vàlid. Trieu 'numpy' o 'scipy'.")
            
            self.x[:, i] = self.x[:, i - 1] + dx
            self.y[:, i] = self.y[:, i - 1] + dy

    def mostrar(self, title="Simulació de Moviment Brownià en 2D", interval=0):
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.subplots_adjust(bottom=0.2)

        def update(val):
            ax.clear()
            try:
                new_interval = int(text_box.text)
            except ValueError:
                new_interval = interval

            for i in range(self.num_particules):
                ax.plot(self.x[i], self.y[i], label=f'Trajectòria {i+1}')
                if new_interval > 0:
                    for j in range(0, self.num_passos, new_interval):
                        ax.text(self.x[i, j], self.y[i, j], f'{self.temps[j]:.2f}', fontsize=8, color='black')

            ax.scatter(self.x[:, 0], self.y[:, 0], color='red', marker='o', label="Inici")
            ax.scatter(self.x[:, -1], self.y[:, -1], color='blue', marker='x', label="Fi")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_title(title)
            ax.legend()
            ax.grid()
            fig.canvas.draw()
        
        ax_textbox = plt.axes([0.2, 0.05, 0.2, 0.075])
        text_box = TextBox(ax_textbox, "Interval", initial=str(interval))
        text_box.on_submit(update)
        update(None)
        plt.show()
