import numpy as np
import matplotlib.pyplot as plt

# Nombre de passos
each_range = 10000
num_steps = 100000
num_traj = 1000

# Moviments possibles: amunt, avall, dreta, esquerra
movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# Generació del camí
x, y = [0], [0] # Inicialització de les coordenades
all_x, all_y = [], []
for _ in range(num_traj):
    x, y = [0], [0]
    for _ in range(num_steps):
        dx, dy = movements[np.random.randint(0, 4)]  # Selecciona un moviment aleatori
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)
    all_x.append(x)
    all_y.append(y)

# Calcular las distancias del punto (0,0) a los puntos n.100, n.200, ..., n.num_steps para cada trayectoria
distances = {i: [] for i in range(each_range, num_steps+1, each_range)}

for i in range(len(all_x)):
    for step in range(each_range, num_steps+1, each_range):
        distance = np.sqrt((all_x[i][step] - all_x[i][0])**2 + (all_y[i][step] - all_y[i][0])**2)
        distances[step].append(distance**2)

# Calcular las medias de las distancias
mean_distances = {step: np.mean(distances[step]) for step in distances}

# Crear el plot
plt.figure(figsize=(10, 6))
plt.plot(list(mean_distances.keys()), list(mean_distances.values()), marker='o', linestyle='-', color='b')
plt.title("Distancia media desde el punto (0,0) a diferentes puntos finales")
plt.xlabel("Punto final (n)")
plt.ylabel("Distancia media")
plt.grid(True)
plt.show()