import cupy as cp
import matplotlib.pyplot as plt

# Nombre de passos
num_steps = 100000
num_traj = 1000

# Moviments possibles: amunt, avall, dreta, esquerra
movements = cp.array([(1, 0), (-1, 0), (0, 1), (0, -1)])

# Generació del camí
# Generació de 1000 trajectòries
all_x, all_y = [], []
for _ in range(num_traj):
    x, y = cp.zeros(num_steps + 1), cp.zeros(num_steps + 1)
    for step in range(1, num_steps + 1):
        dx, dy = movements[cp.random.randint(0, 4)]
        x[step] = x[step - 1] + dx
        y[step] = y[step - 1] + dy
    all_x.append(x)
    all_y.append(y)

# Calcular las distancias del punto (0,0) a los puntos n.100, n.200, ..., n.num_steps para cada trayectoria
distances = {i: [] for i in range(100, num_steps + 1, 100)}

for i in range(len(all_x)):
    for step in range(100, num_steps + 1, 100):
        distance = cp.sqrt((all_x[i][step] - all_x[i][0])**2 + (all_y[i][step] - all_y[i][0])**2)
        distances[step].append(cp.asnumpy(distance))

# Calcular las medias de las distancias
mean_distances = {step: cp.mean(cp.array(distances[step])) for step in distances}

# Crear el plot
plt.figure(figsize=(10, 6))
plt.plot(list(mean_distances.keys()), list(mean_distances.values()), marker='o', linestyle='-', color='b')
plt.title("Distancia media desde el punto (0,0) a diferentes puntos finales")
plt.xlabel("Punto final (n)")
plt.ylabel("Distancia media")
plt.grid(True)
plt.show()
