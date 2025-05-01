import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pickle
import json
import os
from data.DatasetGenerator import DatasetGenerator
from data.specific_datasets.LoadedDataset import LoadedDataset
from analysis.DataAnalyzer import DataAnalyzer

PATH = "./data/"
CONFIG_PATH = "./config/config.json"

class TrajectoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Aplicació de Trajectòries 🚀")
        self.root.geometry("800x600")
        
        # Load configuration
        self.config = self.carregar_configuracio()
        self.num_particules = self.config.get("num_particules", 5)
        self.num_passos = self.config.get("num_passos", 1000)
        
        # Current dataset
        self.current_dataset = None
        
        self.create_main_menu()
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def carregar_configuracio(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r") as config_file:
                return json.load(config_file)
        return {"num_particules": 5, "num_passos": 1000}
    
    def guardar_configuracio(self):
        config = {
            "num_particules": self.num_particules,
            "num_passos": self.num_passos
        }
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w") as config_file:
            json.dump(config, config_file)
    
    def create_main_menu(self):
        self.clear_frame()
        
        title_label = ttk.Label(self.root, text="🌟 Menú Principal 🌟", font=("Helvetica", 16))
        title_label.pack(pady=20)
        
        btn1 = ttk.Button(self.root, text="🚀 Interpretar dataset de trajectòries", 
                          command=self.menu_interpretar_dataset)
        btn1.pack(pady=10, padx=50, fill=tk.X)
        
        exit_btn = ttk.Button(self.root, text="❌ Sortir", command=self.root.quit)
        exit_btn.pack(pady=10, padx=50, fill=tk.X)
    
    def menu_interpretar_dataset(self):
        self.clear_frame()
        
        title_label = ttk.Label(self.root, text="ℹ️ Primer hem de carregar un dataset", font=("Helvetica", 14))
        title_label.pack(pady=20)
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=20)
        
        btn1 = ttk.Button(btn_frame, text="✨ Generar trajectòries", 
                          command=self.menu_tipus_trajectoria)
        btn1.pack(pady=10, fill=tk.X)
        
        btn2 = ttk.Button(btn_frame, text="📂 Carregar trajectòries", 
                          command=self.menu_carregar_trajectoria)
        btn2.pack(pady=10, fill=tk.X)
        
        back_btn = ttk.Button(btn_frame, text="🔙 Tornar enrere", command=self.create_main_menu)
        back_btn.pack(pady=10, fill=tk.X)
    
    def menu_carregar_trajectoria(self):
        self.clear_frame()
        
        title_label = ttk.Label(self.root, text="ℹ️ Si us plau, escolliu un dataset de trajectòries", font=("Helvetica", 14))
        title_label.pack(pady=20)
        
        data_path = os.path.join(os.getcwd(), "data")
        pkl_files = []
        
        if os.path.exists(data_path):
            pkl_files = [file for file in os.listdir(data_path) if file.endswith(".pkl")]
        
        if not pkl_files:
            no_files_label = ttk.Label(self.root, text="⚠️ No hi ha datasets disponibles.")
            no_files_label.pack(pady=20)
        else:
            files_frame = ttk.Frame(self.root)
            files_frame.pack(pady=10, fill=tk.BOTH, expand=True)
            
            scrollbar = ttk.Scrollbar(files_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            listbox = tk.Listbox(files_frame, yscrollcommand=scrollbar.set)
            for idx, file in enumerate(pkl_files, start=1):
                listbox.insert(tk.END, f"{idx}. {file}")
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=listbox.yview)
            
            def load_selected():
                selection = listbox.curselection()
                if selection:
                    selected_file = pkl_files[selection[0]]
                    try:
                        with open(os.path.join(data_path, selected_file), 'rb') as f:
                            self.current_dataset = pickle.load(f)
                        self.dataset_options_menu()
                    except Exception as e:
                        messagebox.showerror("Error", f"Error en carregar el dataset: {e}")
            
            load_btn = ttk.Button(self.root, text="📥 Carregar selecció", command=load_selected)
            load_btn.pack(pady=10)
        
        back_btn = ttk.Button(self.root, text="🔙 Tornar enrere", command=self.menu_interpretar_dataset)
        back_btn.pack(pady=10)
    
    def configurar_parametres(self):
        self.clear_frame()
        
        title_label = ttk.Label(self.root, text="⚙️ Submenú de configuració", font=("Helvetica", 14))
        title_label.pack(pady=20)
        
        # Particles configuration
        particles_frame = ttk.Frame(self.root)
        particles_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(particles_frame, text="🔢 Quantitat de partícules:").pack(side=tk.LEFT)
        self.particles_var = tk.IntVar(value=self.num_particules)
        particles_spin = ttk.Spinbox(particles_frame, from_=1, to=1000, textvariable=self.particles_var)
        particles_spin.pack(side=tk.LEFT, padx=10)
        
        # Steps configuration
        steps_frame = ttk.Frame(self.root)
        steps_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(steps_frame, text="🔄 Quantitat de passos:").pack(side=tk.LEFT)
        self.steps_var = tk.IntVar(value=self.num_passos)
        steps_spin = ttk.Spinbox(steps_frame, from_=1, to=10000, textvariable=self.steps_var)
        steps_spin.pack(side=tk.LEFT, padx=10)
        
        def save_config():
            self.num_particules = self.particles_var.get()
            self.num_passos = self.steps_var.get()
            self.guardar_configuracio()
            messagebox.showinfo("Configuració", "Configuració guardada correctament!")
            self.menu_tipus_trajectoria()
        
        save_btn = ttk.Button(self.root, text="💾 Guardar configuració", command=save_config)
        save_btn.pack(pady=10)
        
        back_btn = ttk.Button(self.root, text="🔙 Tornar enrere", command=self.menu_tipus_trajectoria)
        back_btn.pack(pady=10)
    
    def menu_tipus_trajectoria(self):
        self.clear_frame()
        
        title_label = ttk.Label(self.root, text="ℹ️ Si us plau, configureu els paràmetres de la simulació", font=("Helvetica", 14))
        title_label.pack(pady=20)
        
        config_frame = ttk.Frame(self.root)
        config_frame.pack(pady=10)
        
        ttk.Label(config_frame, text=f"🔢 Quantitat de partícules: {self.num_particules}").pack()
        ttk.Label(config_frame, text=f"🔄 Quantitat de passos: {self.num_passos}").pack()
        
        options_frame = ttk.Frame(self.root)
        options_frame.pack(pady=20)
        
        trajectory_types = [
            ("🚶 Random Walk", "generate_RandomWalk"),
            ("📈 Trajectòria browniana", "generate_BrownianMotion"),
            ("⏱️ Continuous Time Random Walk", "generate_ContinuousTimeRandomWalk"),
            ("📉 Fractional Brownian Motion", "generate_FractionalBrownianMotion"),
            ("🌀 Lévy Walks", "generate_LevyWalks"),
            ("🔄 Annealed Transit Time Model", "generate_AnnealedTransitTimeModel"),
            ("📏 Scaled Brownian Motion", "generate_ScaledBrownianMotion"),
            ("⚙️ Configurar paràmetres", "configurar_parametres")
        ]
        
        for text, command in trajectory_types:
            btn = ttk.Button(options_frame, text=text, 
                            command=lambda cmd=command: self.generate_trajectory(cmd))
            btn.pack(pady=5, fill=tk.X)
        
        back_btn = ttk.Button(self.root, text="🔙 Tornar enrere", command=self.menu_interpretar_dataset)
        back_btn.pack(pady=10)
    
    def generate_trajectory(self, command):
        if command == "configurar_parametres":
            self.configurar_parametres()
            return
        
        dataset_generator = DatasetGenerator(num_particules=self.num_particules)
        try:
            generate_method = getattr(dataset_generator, command)
            self.current_dataset = generate_method(num_passos=self.num_passos)
            self.dataset_options_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Error en generar trajectòria: {e}")
    
    def dataset_options_menu(self):
        self.clear_frame()
        
        title_label = ttk.Label(self.root, text="ℹ️ Dataset carregat correctament", font=("Helvetica", 14))
        title_label.pack(pady=20)
        
        options_frame = ttk.Frame(self.root)
        options_frame.pack(pady=20)
        
        btn1 = ttk.Button(options_frame, text="📊 Anàlisi estadístic", 
                          command=self.statistical_analysis_menu)
        btn1.pack(pady=5, fill=tk.X)
        
        btn2 = ttk.Button(options_frame, text="🤖 Inferir amb un model de IA", 
                          command=self.infer_with_ai)
        btn2.pack(pady=5, fill=tk.X)
        
        btn3 = ttk.Button(options_frame, text="💾 Guardar el dataset", 
                          command=self.save_dataset)
        btn3.pack(pady=5, fill=tk.X)
        
        back_btn = ttk.Button(self.root, text="🔙 Tornar enrere", command=self.menu_interpretar_dataset)
        back_btn.pack(pady=10)
    
    def statistical_analysis_menu(self):
        self.clear_frame()
        
        title_label = ttk.Label(self.root, text="📊 Anàlisi estadístic", font=("Helvetica", 14))
        title_label.pack(pady=20)
        
        analyser = DataAnalyzer(self.current_dataset)
        
        btn1 = ttk.Button(self.root, text="📈 Mostrar trajectòries", 
                          command=analyser.mostrar_trajectories)
        btn1.pack(pady=5, fill=tk.X, padx=50)
        
        btn2 = ttk.Button(self.root, text="📉 Mostrar evolució amb el temps", 
                          command=analyser.mostrar_evolucio)
        btn2.pack(pady=5, fill=tk.X, padx=50)
        
        btn3 = ttk.Button(self.root, text="📊 Mostrar histograma 3D", 
                          command=analyser.mostrar_histograma)
        btn3.pack(pady=5, fill=tk.X, padx=50)
        
        back_btn = ttk.Button(self.root, text="🔙 Tornar enrere", command=self.dataset_options_menu)
        back_btn.pack(pady=10)
    
    def infer_with_ai(self):
        messagebox.showinfo("Informació", "🤖 Funció d'inferència amb IA encara no implementada")
    
    def save_dataset(self):
        name = tk.simpledialog.askstring("Guardar dataset", "Introdueix el nom del dataset:")
        if name:
            try:
                os.makedirs(PATH, exist_ok=True)
                file_path = os.path.join(PATH, f"{name}.pkl")
                with open(file_path, 'wb') as f:
                    pickle.dump(self.current_dataset, f)
                messagebox.showinfo("Èxit", f"✅ Dataset guardat correctament a {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"⚠️ Error en guardar el dataset: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrajectoryApp(root)
    root.mainloop()