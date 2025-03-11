import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from scipy.stats import norm
from config import *
import os
import pandas as pd  # Add pandas import

class TrajectoriesGenerator:
    def __init__(self,
            num_particules=NUM_PARTICULES,
            num_passos=NUM_PASSOS,
            t_inicial=T_INICIAL,
            t_final=T_FINAL
        ):
        self.num_particules = num_particules
        self.num_passos = num_passos
        self.t_inicial = t_inicial
        self.t_final = t_final
        self.x = pd.DataFrame(np.zeros((num_particules, num_passos)))  # Use DataFrame
        self.y = pd.DataFrame(np.zeros((num_particules, num_passos)))  # Use DataFrame
        self.temps = np.linspace(t_inicial, t_final, num_passos)
        self.movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def generate_random_walk(self, tipus = "nonstop"):
        movements = RANDOM_WALK_MOVEMENTS_NONSTOP
        if tipus == "chill_stop": movements = RANDOM_WALK_MOVEMENTS_CHILL_STOP
        elif tipus == "hard_stop": movements = RANDOM_WALK_MOVEMENTS_HARD

        for i in range(1, self.num_passos):
            dx = np.zeros(self.num_particules)
            dy = np.zeros(self.num_particules)
            for j in range(self.num_particules):
                dx[j], dy[j] = movements[np.random.randint(0, len(movements))]
            self.x.iloc[:, i] = self.x.iloc[:, i - 1] + dx
            self.y.iloc[:, i] = self.y.iloc[:, i - 1] + dy

    def generate_brownian_trajectory(self, tipus="numpy", delta_t=DELTA_T, sigma=SIGMA):
        for i in range(1, self.num_passos):
            if tipus == "numpy":
                dx = np.random.normal(0, sigma * np.sqrt(delta_t), self.num_particules)
                dy = np.random.normal(0, sigma * np.sqrt(delta_t), self.num_particules)
            elif tipus == "scipy":
                dx = norm.rvs(loc=0, scale=sigma * np.sqrt(delta_t), size=self.num_particules)
                dy = norm.rvs(loc=0, scale=sigma * np.sqrt(delta_t), size=self.num_particules)
            self.x.iloc[:, i] = self.x.iloc[:, i - 1] + dx
            self.y.iloc[:, i] = self.y.iloc[:, i - 1] + dy
    
    def load_dataset(self, df_x, df_y):
        self.x = df_x
        self.y = df_y

    def mostrar_trajectories(self, title="Simulació de Moviment Brownià en 2D", interval=0):
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.subplots_adjust(bottom=0.2)

        def update(val):
            ax.clear()
            try:
                new_interval = int(text_box.text)
            except ValueError:
                new_interval = interval

            for i in range(self.num_particules):
                ax.plot(self.x.iloc[i], self.y.iloc[i], label=f'Trajectòria {i+1}')
                if new_interval > 0:
                    for j in range(0, self.num_passos, new_interval):
                        ax.text(self.x.iloc[i, j], self.y.iloc[i, j], f'{self.temps[j]:.2f}', fontsize=8, color='black')

            ax.scatter(self.x.iloc[:, 0], self.y.iloc[:, 0], color='red', marker='o', label="Inici")
            ax.scatter(self.x.iloc[:, -1], self.y.iloc[:, -1], color='blue', marker='x', label="Fi")
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
    
    def mostrar_evolucio(self):
        each_range = self.num_passos // 25
        distances = {i: [] for i in range(each_range, self.num_passos+1, each_range)}
        for i in range(self.num_particules):
            for step in range(each_range, self.num_passos+1, each_range):
                distance = np.sqrt((self.x.iloc[i, step-1] - self.x.iloc[i, 0])**2 + (self.y.iloc[i, step-1] - self.y.iloc[i, 0])**2)
                distances[step].append(distance)

        # Calcular las medias de las distancias
        mean_distances = {step: np.mean(distances[step]) for step in distances}

        # Crear el plot
        plt.figure(figsize=(10, 6))
        plt.plot([0] + list(mean_distances.keys()), [0] + list(mean_distances.values()), marker='o', linestyle='-', color='b')
        plt.title("Distancia media desde el punto (0,0) a diferentes puntos finales")
        plt.xlabel("Punto final (n)")
        plt.ylabel("Distancia media")
        plt.grid(True)
        plt.show()

    def get_dataset(self):
        return self.x, self.y