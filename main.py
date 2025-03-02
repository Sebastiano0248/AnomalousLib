import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

# Paràmetres
NUM_PARTICULES = 5  # Nombre de trajectòries
NUM_PASSOS = 1000   # Nombre de passos en el temps
DELTA_T = 1         # Pas de temps
SIGMA = 1           # Desviació estàndard
T_INICIAL = 0       # Temps inicial
T_FINAL = 10        # Temps final

def plot_trajectories(x, y, temps, title, interval=0):
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.2)
    num_particules = x.shape[0]
    num_passos = x.shape[1]
    
    def update(val):
        ax.clear()
        try:
            new_interval = int(text_box.text)
        except ValueError:
            new_interval = interval  # Mantenir el valor per defecte si l'entrada no és vàlida
        
        for i in range(num_particules):
            ax.plot(x[i], y[i], label=f'Trajectòria {i+1}')
            if new_interval > 0:
                for j in range(0, num_passos, new_interval):
                    ax.text(x[i, j], y[i, j], f'{temps[j]:.2f}', fontsize=8, color='black')
        
        ax.scatter(x[:, 0], y[:, 0], color='red', marker='o', label="Inici")
        ax.scatter(x[:, -1], y[:, -1], color='blue', marker='x', label="Fi")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(title)
        ax.legend()
        ax.grid()
        fig.canvas.draw()
    
    ax_textbox = plt.axes([0.2, 0.05, 0.2, 0.075])
    text_box = TextBox(ax_textbox, "Interval", initial=str(interval))
    text_box.on_submit(update)
    
    update(None)  # Dibuixar el gràfic inicialment
    plt.show()

def trajGeneratorByNumpy(num_particules=NUM_PARTICULES, num_passos=NUM_PASSOS, delta_t=DELTA_T, sigma=SIGMA, t_inicial=T_INICIAL, t_final=T_FINAL):
    x = np.zeros((num_particules, num_passos))
    y = np.zeros((num_particules, num_passos))
    temps = np.linspace(t_inicial, t_final, num_passos)

    for i in range(1, num_passos):
        dx = np.random.normal(0, sigma * np.sqrt(delta_t), num_particules)
        dy = np.random.normal(0, sigma * np.sqrt(delta_t), num_particules)
        x[:, i] = x[:, i - 1] + dx
        y[:, i] = y[:, i - 1] + dy

    plot_trajectories(x, y, temps, "Simulació de Moviment Brownià en 2D")

def trajGeneratorByScipy(num_particules=NUM_PARTICULES, num_passos=NUM_PASSOS, delta_t=DELTA_T, sigma=SIGMA, t_inicial=T_INICIAL, t_final=T_FINAL):
    from scipy.stats import norm
    x = np.zeros((num_particules, num_passos))
    y = np.zeros((num_particules, num_passos))
    temps = np.linspace(t_inicial, t_final, num_passos)

    for i in range(1, num_passos):
        dx = norm.rvs(loc=0, scale=sigma * np.sqrt(delta_t), size=num_particules)
        dy = norm.rvs(loc=0, scale=sigma * np.sqrt(delta_t), size=num_particules)
        x[:, i] = x[:, i - 1] + dx
        y[:, i] = y[:, i - 1] + dy

    plot_trajectories(x, y, temps, "Moviment Brownià amb scipy.stats")

if __name__ == "__main__":
    print("Seleccioneu una opció:")
    print("1. Generar trajectòries amb Numpy")
    print("2. Generar trajectòries amb Scipy")
    opcio = input("Introduïu el número de l'opció desitjada: ")

    if opcio == "1":
        trajGeneratorByNumpy()
    elif opcio == "2":
        trajGeneratorByScipy()
    else:
        print("Opció no vàlida")
