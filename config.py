NUM_PARTICULES = 5  # Nombre de trajectòries
NUM_PASSOS = 1000   # Nombre de passos en el temps

# Constants del Random Walk
RANDOM_WALK_MOVEMENTS_NONSTOP = [(1, 0), (-1, 0), (0, 1), (0, -1)]
RANDOM_WALK_MOVEMENTS_CHILL_STOP = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
RANDOM_WALK_MOVEMENTS_HARD = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0), (0, 0), (0, 0), (0, 0)]

# Paràmetres del moviment Brownià
DELTA_T = 1         # Pas de temps
SIGMA = 1           # Desviació estàndard
T_INICIAL = 0       # Temps inicial
T_FINAL = 10        # Temps final
