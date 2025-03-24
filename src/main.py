from data.specific_datasets import GeneratedDataset, RealDataset

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_carregar_dataset():
    print("1. ✨ Generar trajectòries")
    print("2. 📂 Carregar trajectòries")
    print()
    print("0. ❌ Tornar enrere")
    opcio = input("Seleccioneu una opció: ")
    dataset = None
    while dataset is None:
        if opcio == "1":
            dataset = GeneratedDataset().load()
        elif opcio == "2":
            dataset = RealDataset()
        elif opcio == "0":
            return
        else:
            print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
            opcio = input("Seleccioneu una opció: ")

print("🚀 Benvinguts a l'aplicació de trajectòries 🚀co")
while True:
    clear_screen()
    print("🌟 Menú Principal 🌟")
    print("1. 🚀 Carregar dataset de trajectòries")
    print("2. 🔍 Interpretar trajectòries")
    # 3. Veure resultats
    print()
    print("0. ❌ Sortir")
    
    opcio = input("Seleccioneu una opció: ")
    
    if opcio == "1":
        clear_screen()
        menu_carregar_dataset()
    elif opcio == "2":
        clear_screen()
        print("🔍 Interpretant trajectòries...")
        # Lògica per interpretar trajectòries
    elif opcio == "0":
        clear_screen()
        print("❌ Sortint del programa...")
        break
    else:
        clear_screen()
        print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")

def menu_carregar_dataset():
    print("1. ✨ Generar trajectòries")
    print("2. 📂 Carregar trajectòries")
    print()
    print("0. ❌ Tornar enrere")
    opcio = input("Seleccioneu una opció: ")
    dataset = None
    while dataset is None:
        if opcio == "1":
            print("✨ Generant trajectòries...")
            dataset = GeneratedDataset().load()
        elif opcio == "2":
            print("📂 Carregant trajectòries...")
            dataset = RealDataset()
        elif opcio == "0":
            return
        else:
            print("⚠️ Opció no vàlida. Si us plau, torneu-ho a intentar.")
            opcio = input("Seleccioneu una opció: ")
