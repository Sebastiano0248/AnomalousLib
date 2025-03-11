import os
import pandas as pd
from TrajectoriesGenerator import TrajectoriesGenerator



def guardar_dades(traj):
        nom_dades = input("Introduïu el nom de les dades (no posi res per a no per defecte): ")
        if nom_dades == "": nom_dades = None
        df_x, df_y = traj.get_dataset()
        
        if nom_dades is None:
            directory_x = 1
            while os.path.exists(f'trajectories/traj_{directory_x}'):
                directory_x += 1
            directory_name = f'trajectories/traj_{directory_x}'
        else:
            directory_name = f'trajectories/{nom_dades}'
        
        os.makedirs(directory_name, exist_ok=True)
        
        # Guardar los DataFrames en archivos CSV dentro de la subcarpeta
        df_x.to_csv(f'{directory_name}/trajectory_x.csv', index=False)
        df_y.to_csv(f'{directory_name}/trajectory_y.csv', index=False)

        df_x.to_feather(f'{directory_name}/trajectory_x.feather')
        df_y.to_feather(f'{directory_name}/trajectory_y.feather')

def carregar_dataset(traj):
    nom_dades = input("Introduïu el nom de les dades: ")
    df_x = pd.read_feather(f'trajectories/{nom_dades}/trajectory_x.feather')
    df_y = pd.read_feather(f'trajectories/{nom_dades}/trajectory_y.feather')
    traj.load_dataset(df_x, df_y)

if __name__ == "__main__":
    print("Seleccioneu una opció:")
    print("1. Generar trajectòries de tipus Random Walk")
    print("2. Generar trajectòries amb Numpy")
    print("3. Generar trajectòries amb Scipy")
    print("4. Carregar dades")
    
    opcio = input("Introduïu el número de l'opció desitjada: ")

    traj = TrajectoriesGenerator(num_particules=1000, num_passos=100000)

    if opcio == "1":
        traj.generate_random_walk(tipus="hard_stop")
    elif opcio == "2":
        traj.generate_brownian_trajectory(tipus="numpy")
    elif opcio == "3":
        traj.generate_brownian_trajectory(tipus="scipy")
    elif opcio == "4":
        carregar_dataset(traj)
    else:
        print("Opció no vàlida")
        exit()

    while True:
        print("Seleccioneu una opció:")
        print("1. Mostrar trajectòries")
        print("2. Mostrar evolució amb el temps")
        print("3. Guardar dades")
        print("4. Sortir")
        
        sub_opcio = input("Introduïu el número de l'opció desitjada: ")

        if sub_opcio == "1":
            traj.mostrar_trajectories()
        elif sub_opcio == "2":
            traj.mostrar_evolucio()
        elif sub_opcio == "3":
            guardar_dades(traj)
        elif sub_opcio == "4":
            print("Sortint...")
            break
        else:
            print("Opció no vàlida")