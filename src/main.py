from data.DatasetGenerator import DatasetGenerator
from analysis.DataAnalyzer import DataAnalyzer
from utils.helpers import load_param

import customtkinter
import os
import pickle
import json

class TrajectoriesApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Anàlisi de Trajectòries")
        
        # Configurar el directorio de datos
        self.data_dir = load_param("path", "dataset>generated")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Marco principal
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.show_main_menu()

    def clear_frame(self, frame=None):
        frame = frame or self.main_frame
        for widget in frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_frame()
        self.title("Menú Principal")
        
        title = customtkinter.CTkLabel(self.main_frame, 
                                     text="🌟 Menú Principal 🌟",
                                     font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        btn_style = {"font": ("Arial", 16), "width": 300, "height": 40}
        
        customtkinter.CTkButton(self.main_frame, 
                              text="🚀 Interpretar dataset",
                              command=self.show_interpret_menu,
                              **btn_style).pack(pady=10)
        
        customtkinter.CTkButton(self.main_frame, 
                              text="❌ Sortir",
                              command=self.quit,
                              **btn_style).pack(pady=10)

    def show_interpret_menu(self):
        self.clear_frame()
        self.title("Interpretar Dataset")
        
        title = customtkinter.CTkLabel(self.main_frame, 
                                     text="📂 Opcions de Dataset",
                                     font=("Arial", 22, "bold"))
        title.pack(pady=20)
        
        btn_style = {"font": ("Arial", 14), "width": 250, "height": 35}
        
        customtkinter.CTkButton(self.main_frame,
                              text="✨ Generar nou dataset",
                              command=self.show_generation_menu,
                              **btn_style).pack(pady=10)
        
        customtkinter.CTkButton(self.main_frame,
                              text="📂 Carregar existent",
                              command=self.show_load_menu,
                              **btn_style).pack(pady=10)
        
        self.back_button(self.show_main_menu)

    def show_generation_menu(self):
        self.clear_frame()
        self.title("Generar Dataset")
        
        config = self.load_config()
        
        title = customtkinter.CTkLabel(self.main_frame, 
                                     text="⚙️ Tipus de Trajectòria",
                                     font=("Arial", 22, "bold"))
        title.pack(pady=15)
        
        # Mostrar configuración actual
        config_label = customtkinter.CTkLabel(self.main_frame,
                                            text=f"Configuració actual:\n"
                                                 f"Partícules: {config['num_particules']} | "
                                                 f"Passos: {config['num_passos']} | "
                                                 f"Passos: {config['random_params']}")
        config_label.pack(pady=10)
        
        # Botón de configuración
        customtkinter.CTkButton(self.main_frame,
                              text="⚙️ Configurar paràmetres",
                              command=self.show_config_menu,
                              width=200).pack(pady=5)

        # Tipos de trayectorias
        trajectories = [
            ("🚶 Random Walk", "generate_RandomWalk"),
            ("📈 Brownian Motion", "generate_BrownianMotion"),
            ("⏱️ CTRW", "generate_ContinuousTimeRandomWalk"),
            ("📉 FBM", "generate_FractionalBrownianMotion"),
            ("🌀 Lévy Walks", "generate_LevyWalks"),
            ("🔄 ATTM", "generate_AnnealedTransitTimeModel"),
            ("📏 SBM", "generate_ScaledBrownianMotion")
        ]
        
        for text, method in trajectories:
            customtkinter.CTkButton(self.main_frame,
                                  text=text,
                                  command=lambda m=method: self.generate_dataset(m),
                                  width=250).pack(pady=3)
        
        self.back_button()

    def show_config_menu(self):
        self.clear_frame()
        self.title("Configuració")
        
        config = self.load_config()
        
        title = customtkinter.CTkLabel(self.main_frame, 
                                     text="⚙️ Configuració de Paràmetres",
                                     font=("Arial", 22, "bold"))
        title.pack(pady=20)
        
        # Entradas para parámetros
        input_style = {"font": ("Arial", 14), "width": 200}
        
        customtkinter.CTkLabel(self.main_frame, 
                             text="Nombre de partícules:").pack()
        self.particles_entry = customtkinter.CTkEntry(self.main_frame, 
                                                    **input_style)
        self.particles_entry.insert(0, str(config["num_particules"]))
        self.particles_entry.pack(pady=5)
        
        customtkinter.CTkLabel(self.main_frame, 
                             text="Nombre de passos:").pack()
        self.steps_entry = customtkinter.CTkEntry(self.main_frame, 
                                                **input_style)
        self.steps_entry.insert(0, str(config["num_passos"]))
        self.steps_entry.pack(pady=5)

        customtkinter.CTkLabel(self.main_frame, 
                     text="Paràmetres aleatoris:").pack()
        self.random_params_var = customtkinter.BooleanVar(value=config["random_params"])
        self.random_params_checkbox = customtkinter.CTkCheckBox(self.main_frame, 
                                      text="Activar",
                                      variable=self.random_params_var)
        self.random_params_checkbox.pack(pady=5)
        
        customtkinter.CTkButton(self.main_frame,
                              text="💾 Guardar Configuració",
                              command=self.save_config).pack(pady=15)
        
        self.back_button()

    def show_load_menu(self):
        self.clear_frame()
        self.title("Carregar Dataset")
        
        title = customtkinter.CTkLabel(self.main_frame, 
                                     text="📂 Datasets Disponibles",
                                     font=("Arial", 22, "bold"))
        title.pack(pady=20)
        
        # Listar archivos .pkl
        files = [f for f in os.listdir(self.data_dir) if f.endswith(".pkl")]
        
        if not files:
            customtkinter.CTkLabel(self.main_frame, 
                                 text="No s'han trobat datasets").pack()
        else:
            for idx, filename in enumerate(files, 1):
                customtkinter.CTkButton(self.main_frame,
                                      text=f"{idx}. {filename}",
                                      command=lambda f=filename: self.load_dataset(f),
                                      width=300).pack(pady=3)
        
        self.back_button()

    def show_analysis_menu(self, dataset):
        self.clear_frame()
        self.title("Anàlisi")
        
        title = customtkinter.CTkLabel(self.main_frame, 
                                     text="📊 Opcions d'Anàlisi",
                                     font=("Arial", 22, "bold"))
        title.pack(pady=20)
        
        btn_style = {"width": 250, "height": 35}
        
        customtkinter.CTkButton(self.main_frame,
                              text="📈 Mostrar Trajectòries",
                              command=lambda: DataAnalyzer(dataset).mostrar_trajectories(),
                              **btn_style).pack(pady=5)
        
        customtkinter.CTkButton(self.main_frame,
                              text="📉 Evolució Temporal",
                              command=lambda: DataAnalyzer(dataset).mostrar_evolucio(),
                              **btn_style).pack(pady=5)
        
        customtkinter.CTkButton(self.main_frame,
                              text="📊 Histograma 3D",
                              command=lambda: DataAnalyzer(dataset).mostrar_histograma(),
                              **btn_style).pack(pady=5)
        
        customtkinter.CTkButton(self.main_frame,
                              text="💾 Guardar Dataset",
                              command=lambda: self.show_save_menu(dataset),
                              **btn_style).pack(pady=15)
        
        self.back_button()

    def show_save_menu(self, dataset):
        self.clear_frame()
        self.title("Guardar Dataset")
        
        title = customtkinter.CTkLabel(self.main_frame, 
                                     text="💾 Guardar Dataset",
                                     font=("Arial", 22, "bold"))
        title.pack(pady=20)
        
        self.filename_entry = customtkinter.CTkEntry(self.main_frame,
                                                   width=300,
                                                   placeholder_text="Nom del fitxer")
        self.filename_entry.pack(pady=10)
        
        customtkinter.CTkButton(self.main_frame,
                              text="Guardar",
                              command=lambda: self.save_dataset(dataset),
                              width=150).pack(pady=10)
        
        self.back_button()

    def back_button(self, command=None):
        customtkinter.CTkButton(self.main_frame,
                              text="🔙 Tornar",
                              command=command or self.show_interpret_menu,
                              width=100).pack(pady=15)

    # Funcionalidades principales
    
    def load_config(self):
        try:
            with open("config/config.json") as f:
                return json.load(f)
        except:
            return {"num_particules": 5, "num_passos": 1000}

    def save_config(self):
        try:
            config = {
                "num_particules": int(self.particles_entry.get()),
                "num_passos": int(self.steps_entry.get()),
                "random_params": int(self.random_params_checkbox.get())
            }
            os.makedirs("config", exist_ok=True)
            with open("config/config.json", "w") as f:
                json.dump(config, f)
            self.show_generation_menu()
        except ValueError:
            error_label = customtkinter.CTkLabel(self.main_frame, 
                                               text="⛔ Valors no vàlids!")
            error_label.pack()

    def generate_dataset(self, method_name):
        config = self.load_config()
        generator = DatasetGenerator(config["num_particules"])   
        try:
            method = getattr(generator, method_name)
            dataset = method(num_passos = config["num_passos"], random_params = config["random_params"])
            self.show_analysis_menu(dataset)
        except Exception as e:
            error_label = customtkinter.CTkLabel(self.main_frame, 
                                               text=f"⛔ Error: {str(e)}")
            error_label.pack()

    def load_dataset(self, filename):
        try:
            with open(os.path.join(self.data_dir, filename), "rb") as f:
                dataset = pickle.load(f)
            self.show_analysis_menu(dataset)
        except Exception as e:
            error_label = customtkinter.CTkLabel(self.main_frame, 
                                               text=f"⛔ Error: {str(e)}")
            error_label.pack()

    def save_dataset(self, dataset):
        filename = self.filename_entry.get()
        if not filename.endswith(".pkl"):
            filename += ".pkl"
        try:
            with open(os.path.join(self.data_dir, filename), "wb") as f:
                pickle.dump(dataset, f)
            success_label = customtkinter.CTkLabel(self.main_frame, 
                                                 text="✅ Dataset guardat!")
            success_label.pack()
        except Exception as e:
            error_label = customtkinter.CTkLabel(self.main_frame, 
                                               text=f"⛔ Error: {str(e)}")
            error_label.pack()

if __name__ == "__main__":
    app = TrajectoriesApp()
    app.mainloop()
    
