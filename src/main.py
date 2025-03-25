from data.specific_datasets.GeneratedDataset import GeneratedDataset
from data.specific_datasets.ImportedDataset import ImportedDataset
from analysis.DataAnalyzer import DataAnalyzer

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_carregar_trajectoria():
    clear_screen()
    print("ℹ️ Si us plau, escolliu un dataset de trajectòries:")
    print()
    dataset = None
    base_path = os.path.join(os.getcwd(), "data")
    raw_path = os.path.join(base_path, "raw")
    generated_path = os.path.join(base_path, "generated")
    
    while dataset is None:
        print("📂 Datasets disponibles:")
        print("1. 🌟 Datasets generats:")
        if os.path.exists(generated_path):
            for idx, file in enumerate(os.listdir(generated_path), start=1):
                print(f"   {idx}. {file}")
        else:
            print("   ⚠️ No hi ha datasets generats disponibles.")
        
        print("2. 🌟 Datasets reals:")
        if os.path.exists(raw_path):
            for idx, file in enumerate(os.listdir(raw_path), start=1):
                print(f"   {idx + len(os.listdir(generated_path))}. {file}")
        else:
            print("   ⚠️ No hi ha datasets reals disponibles.")
        
        print()
        print("0. ❌ Tornar enrere")
        opcio = input("Seleccioneu una opció: ")
        
        try:
            opcio = int(opcio)
            if opcio == 0:
                clear_screen()
                return
            elif 1 <= opcio <= len(os.listdir(generated_path)):
                selected_file = os.listdir(generated_path)[opcio - 1]
                dataset = GeneratedDataset()
                dataset.load(os.path.join(generated_path, selected_file))
            elif len(os.listdir(generated_path)) < opcio <= len(os.listdir(generated_path)) + len(os.listdir(raw_path)):
                selected_file = os.listdir(raw_path)[opcio - len(os.listdir(generated_path)) - 1]
                dataset = ImportedDataset()
                dataset.load(os.path.join(raw_path, selected_file))
            else:
                clear_screen()
                print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
                print()
        except (ValueError, IndexError):
            clear_screen()
            print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
            print()
    return dataset

def menu_tipus_trajectoria():
    clear_screen()
    print("ℹ️ Si us plau, escolliu un tipus de trajectòria:")
    print()
    dataset = None
    while dataset is None:
        print("1. 🚶 Random Walk")
        print("2. 📈 Trajectòria browniana")
        print()
        print("0. ❌ Tornar enrere")
        opcio = input("Seleccioneu una opció: ")
        
        if opcio == "1":
            dataset = GeneratedDataset()
            dataset.generate_random_walk()
        elif opcio == "2":
            dataset = GeneratedDataset()
            dataset.generate_brownian_trajectory()
        elif opcio == "0":
            clear_screen()
            return
        else:
            clear_screen()
            print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
            print()
    return dataset

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
            dataset.change_name(name)
            try:
                dataset.save()
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