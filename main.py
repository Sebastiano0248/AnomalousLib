import os
from Trajectories.TrajectoriesManager import TrajectoriesManager

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

while True:
    clear_screen()
    print("🌟 Menú Principal 🌟")
    print("1. ✨ Generar trajectòries")
    print("2. 🔍 Interpretar trajectòries")
    print()
    print("0. ❌ Sortir")
    
    opcio = input("Seleccioneu una opció: ")
    
    if opcio == "1":
        clear_screen()
        TrajectoriesManager().run()
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