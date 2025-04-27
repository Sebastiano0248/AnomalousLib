from data.DatasetGenerator import DatasetGenerator
from data.specific_datasets.LoadedDataset import LoadedDataset
from analysis.DataAnalyzer import DataAnalyzer

import pickle
import json
import os

PATH = "./data/"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_carregar_trajectoria():
    clear_screen()
    print("ℹ️ Si us plau, escolliu un dataset de trajectòries:")
    print()
    dataset = None
    data_path = os.path.join(os.getcwd(), "data")
    
    while dataset is None:
        print("📂 Datasets disponibles:")
        if os.path.exists(data_path):
            pkl_files = [file for file in os.listdir(data_path) if file.endswith(".pkl")]
            if pkl_files:
                for idx, file in enumerate(pkl_files, start=1):
                    print(f"   {idx}. {file}")
            else:
                print("   ⚠️ No hi ha datasets disponibles.")
        else:
            print("   ⚠️ La carpeta de dades no existeix.")
        
        print()
        print("0. ❌ Tornar enrere")
        opcio = input("Seleccioneu una opció: ")
        
        try:
            opcio = int(opcio)
            if opcio == 0:
                clear_screen()
                return
            elif 1 <= opcio <= len(pkl_files):
                selected_file = pkl_files[opcio - 1]
                with open(os.path.join(data_path, selected_file), 'rb') as f:
                    dataset = pickle.load(f)
            else:
                clear_screen()
                print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
                print()
        except (ValueError, IndexError):
            clear_screen()
            print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
            print()
    return dataset

def configurar_parametres():
    num_particules = 5
    num_passos = 1000
    
    while True:
        clear_screen()
        print("⚙️ Submenú de configuració:")
        print(f"1. 🔢 Quantitat de partícules (actual: {num_particules})")
        print(f"2. 🔄 Quantitat de passos (actual: {num_passos})")
        print()
        print("0. 🔙 Tornar al menú anterior")
        sub_opcio = input("Seleccioneu una opció: ")
        
        if sub_opcio == "1":
            try:
                num_particules = int(input("Introduïu la nova quantitat de partícules: "))
                if num_particules <= 0:
                    raise ValueError
            except ValueError:
                print("⚠️ Valor no vàlid. Si us plau, introduïu un número enter positiu.")
        elif sub_opcio == "2":
            try:
                num_passos = int(input("Introduïu la nova quantitat de passos: "))
                if num_passos <= 0:
                    raise ValueError
            except ValueError:
                print("⚠️ Valor no vàlid. Si us plau, introduïu un número enter positiu.")
        elif sub_opcio == "0":
            break
        else:
            print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
    return num_particules, num_passos

def guardar_configuracio(num_particules, num_passos):
    config_path = os.path.join("config", "config.json")
    config = {
        "num_particules": num_particules,
        "num_passos": num_passos
    }
    with open(config_path, "w") as config_file:
        json.dump(config, config_file)

def carregar_configuracio():
    config_path = os.path.join("config", "config.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            return json.load(config_file)
    return {"num_particules": 5, "num_passos": 1000}

def menu_tipus_trajectoria():
    clear_screen()
    print("ℹ️ Si us plau, configureu els paràmetres de la simulació:")
    print()
    
    config = carregar_configuracio()
    num_particules, num_passos = config["num_particules"], config["num_passos"]
    
    while True:
        print("⚙️ Configuració actual:")
        print(f"   🔢 Quantitat de partícules: {num_particules}")
        print(f"   🔄 Quantitat de passos: {num_passos}")
        print()
        print("1. 🚶 Random Walk")
        print("2. 📈 Trajectòria browniana")
        print("3. ⏱️ Continuous Time Random Walk")
        print("4. 📉 Fractional Brownian Motion")
        print("5. 🌀 Lévy Walks")
        print("6. 🔄 Annealed Transit Time Model")
        print("7. 📏 Scaled Brownian Motion")
        print("8. ⚙️ Configurar paràmetres")
        print()
        print("0. ❌ Tornar enrere")
        opcio = input("Seleccioneu una opció: ")
        
        datasetgenerator = DatasetGenerator(num_particules=num_particules, num_passos=num_passos)
        if opcio == "1":
            dataset = datasetgenerator.generate_RandomWalk()
        elif opcio == "2":
            dataset = datasetgenerator.generate_BrownianMotion()
        elif opcio == "3":
            dataset = datasetgenerator.generate_ContinuousTimeRandomWalk()
        elif opcio == "4":
            dataset = datasetgenerator.generate_FractionalBrownianMotion()
        elif opcio == "5":
            dataset = datasetgenerator.generate_LevyWalks()
        elif opcio == "6":
            dataset = datasetgenerator.generate_AnnealedTransitTimeModel()
        elif opcio == "7":
            dataset = datasetgenerator.generate_ScaledBrownianMotion()
        elif opcio == "8":
            num_particules, num_passos = configurar_parametres()
            guardar_configuracio(num_particules, num_passos)
        elif opcio == "0":
            clear_screen()
            return
        else:
            clear_screen()
            print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
        
        if not opcio in ["8", "0"]: return dataset

def menu_interpretar_dataset():
    clear_screen()
    print("ℹ️ Primer hem de carregar un dataset.")
    print()
    dataset = None
    while dataset is None:
        print("1. ✨ Generar trajectòries")
        print("2. 📂 Carregar trajectòries")
        print()
        print("0. ❌ Tornar enrere")
        opcio = input("Seleccioneu una opció: ")
        if opcio == "1":
            dataset = menu_tipus_trajectoria()
        elif opcio == "2":
            dataset = menu_carregar_trajectoria()
        elif opcio == "0":
            clear_screen()
            return
        else:
            clear_screen()
            print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
            print()
    
    clear_screen()
    print("ℹ️ Dataset carregat correctament.")
    print()

    while True:
        print("🔍 Què vols fer amb el dataset?")
        print("1. 📊 Anàlisi estadístic")
        print("2. 🤖 Inferir amb un model de IA")
        print("3. 💾 Guardar el dataset")
        print()
        print("0. ❌ Tornar enrere")
        opcio = input("Seleccioneu una opció: ")
        
        if opcio == "1":
            statistical_analysis(dataset)
        elif opcio == "2":
            print("🤖 Inferint amb un model de IA...")
            # dataset.infer_with_ai_model()
        elif opcio == "3":
            print("💾 Guardant el dataset...")
            name = input("Introdueix el nom del dataset: ")
            print(dataset)
            try:
                file_path = os.path.join(PATH, f"{name}.pkl")
                print(file_path)
                with open(file_path, 'wb') as f:
                    pickle.dump(dataset, f)
                print(f"✅ Dataset guardat correctament")
            except Exception as e:
                print(f"⚠️ Error en guardar el dataset: {e}")
        elif opcio == "0":
            print("❌ Tornant enrere...")
            break
        else:
            print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")

def statistical_analysis(dataset):
    clear_screen()
    print("📊 Anàlisi estadístic")
    print()
    while True:
        print("Seleccioneu una opció:")
        print("1. Mostrar trajectòries")
        print("2. Mostrar evolució amb el temps")
        print("3. Mostrar histograma 3D")
        print()
        print("0. ❌ Tornar enrere")
        
        opcio = input("Seleccioneu una opció: ")
        analyser = DataAnalyzer(dataset)
        if opcio == "1":
            print("📈 Mostrant trajectòries...")
            analyser.mostrar_trajectories()
        elif opcio == "2":
            print("📉 Mostrant evolució amb el temps...")
            analyser.mostrar_evolucio()
        elif opcio == "3":
            print("📊 Mostrant histograma 3D...")
            analyser.mostrar_histograma()
        elif opcio == "0":
            print("❌ Tornant enrere...")
            break
        else:
            clear_screen()
            print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
            print()

clear_screen()
print("🚀 Benvinguts a l'aplicació de trajectòries 🚀")
print()
while True:
    print("🌟 Menú Principal 🌟")
    print("1. 🚀 Interpretar dataset de trajectòries")
    # print("2. 🔍 Interpretar trajectòries")
    # 3. Veure resultats
    print()
    print("0. ❌ Sortir")
    
    opcio = input("Seleccioneu una opció: ")
    
    if opcio == "1":
        menu_interpretar_dataset()
    elif opcio == "2":
        print("🔍 Interpretant trajectòries...")
        # Lògica per interpretar trajectòries
    elif opcio == "0":
        clear_screen()
        print("❌ Sortint del programa...")
        break
    else:
        clear_screen()
        print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
        print()

print("👋 Fins aviat! 👋")