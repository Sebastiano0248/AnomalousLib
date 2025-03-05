from trajectoryGenerator import TrajectoryGenerator
from config import NUM_PARTICULES, NUM_PASSOS, DELTA_T, SIGMA, T_INICIAL, T_FINAL

if __name__ == "__main__":
    print("Seleccioneu una opció:")
    print("1. Generar trajectòries amb Numpy")
    print("2. Generar trajectòries amb Scipy")
    opcio = input("Introduïu el número de l'opció desitjada: ")

    if opcio == "1":
        generador = TrajectoryGenerator(method="numpy", num_particules=NUM_PARTICULES, num_passos=NUM_PASSOS, delta_t=DELTA_T, sigma=SIGMA, t_inicial=T_INICIAL, t_final=T_FINAL)
    elif opcio == "2":
        generador = TrajectoryGenerator(method="scipy", num_particules=NUM_PARTICULES, num_passos=NUM_PASSOS, delta_t=DELTA_T, sigma=SIGMA, t_inicial=T_INICIAL, t_final=T_FINAL)
    else:
        print("Opció no vàlida")
        exit()
    
    generador.mostrar()
