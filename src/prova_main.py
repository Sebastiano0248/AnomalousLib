from data.DatasetGenerator import DatasetGenerator
from analysis.DataAnalyzer import DataAnalyzer
from utils.helpers import load_param
from utils.constants import styles

import customtkinter
import pickle
import json
import os

# # Configurar el directorio de datos

# self.data_dir = load_param("path", "dataset>generated")
# os.makedirs(self.data_dir, exist_ok=True)

class TrajectoriesApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Marc principal
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Variables globals
        self.default_dataset_config = self._load_default_dataset_config()
        self.data_dir = load_param("path", "dataset>generated")
        
        self.show_main_menu()

    def _load_default_dataset_config(self):
        try:
            with open("config/config.json") as f:
                return json.load(f)
        except:
            return {"num_particules": 5, "num_passos": 1000}

    def _clear_frame(self, frame=None):
        frame = frame or self.main_frame
        for widget in frame.winfo_children():
            widget.destroy()

    def _create_menu_title(self, text, father_frame=None, style=None, pady=20):
        style = style or styles.title_style
        frame = father_frame or self.main_frame
        title = customtkinter.CTkLabel(frame, text=text, **style)
        title.pack(pady=pady)
        return title

    def _create_menu_button(self, text, command, father_frame=None, pady=10, style=None):
        style = style or styles.btn_style
        frame = father_frame or self.main_frame
        button = customtkinter.CTkButton(frame, text=text, command=command, **style)
        button.pack(pady=pady)
        return button
    
    def _create_input_box(self, default_value="", father_frame=None, input_style=None, pady=5):
        input_style = input_style or styles.input_style
        frame = father_frame or self.main_frame
        entry = customtkinter.CTkEntry(frame, **input_style)
        entry.insert(0, str(default_value))
        entry.pack(pady=pady)
        return entry
    
    def _create_check_box(self, default_value=False, text="Activar", father_frame=None, pady=5):
        frame = father_frame or self.main_frame
        var = customtkinter.BooleanVar(value=default_value)
        checkbox = customtkinter.CTkCheckBox(frame, text=text, variable=var)
        checkbox.pack(pady=pady)
        return var, checkbox
    
    def _create_frame(self, father_frame=None, width=200, height=200, pady=10):
        frame = father_frame or self.main_frame
        frame_widget = customtkinter.CTkFrame(frame, width=width, height=height)
        frame_widget.pack(pady=pady)
        frame_widget.pack_propagate(False)
        return frame_widget
        
    def _generate_dataset(self, method_name):
        generator = DatasetGenerator(self.default_dataset_config["num_particules"])   
        try:
            method = getattr(generator, method_name)
            dataset = method(
                num_passos = self.default_dataset_config["num_passos"],
                random_params = self.default_dataset_config["random_params"]
            )
            self.show_save_menu(dataset)
        except Exception as e:
            self._create_menu_title(
                text=f"⛔ Error: {str(e)}",
                style=styles.subtitle_style,
                pady=10
            )
    
    def _save_config(self):
        try:
            # Actualitzar la variable de configuració
            self.default_dataset_config["num_particules"] = int(self.num_particules.get())
            self.default_dataset_config["num_passos"] = int(self.num_passos.get())
            self.default_dataset_config["random_params"] = int(self.random_params.get())

            config = {
                "num_particules": int(self.num_particules.get()),
                "num_passos": int(self.num_passos.get()),
                "random_params": int(self.random_params.get())
            }
            os.makedirs("config", exist_ok=True)
            with open("config/config.json", "w") as f:
                json.dump(config, f)
            self.show_generation_menu()
        except ValueError:
            self._create_menu_title(
                text=f"⛔ Valors no vàlids!",
                style=styles.subtitle_style,
                pady=10
            )

    def show_main_menu(self):
        self._clear_frame()
        self.title("Menú Principal")

        self._create_menu_title("🌟 Menú Principal 🌟")

        self._create_menu_button(
            "✨ Generar dataset",
            self.show_generation_menu
        )
        self._create_menu_button(
            "🚀 Interpretar dataset",
            self.show_load_menu
        )

        self._create_menu_button("❌ Sortir", self.quit)

    def show_generation_menu(self):
        self._clear_frame()
        self.title("Generar Dataset")

        self._create_menu_title("⚙️ Tipus de Trajectòria")

        config_frame = self._create_frame(width=300, height=100)

        self._create_menu_title(
            "Configuració actual:",
            father_frame=config_frame,
            style={"font": ("Arial", 16, "bold"), "anchor": "w", "width": 100},
        ).pack(pady=(5, 0), padx=10, anchor="w")

        self._create_menu_title(
            text=(
                f"• Partícules: {self.default_dataset_config['num_particules']}\n"
                f"• Passos: {self.default_dataset_config['num_passos']}\n"
                f"• Paràmetres aleatoris: {'Sí' if self.default_dataset_config.get('random_params', False) else 'No'}"
            ),
            father_frame=config_frame,
            style={"font": ("Arial", 14), "anchor": "w", "justify": "left", "width": 100},
        ).pack(pady=(0, 5), padx=20, anchor="w")
        
        # Botó de configuració
        self._create_menu_button(
            "⚙️ Configurar paràmetres",
            self.show_config_menu
        )

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
            self._create_menu_button(
                text=text, pady=5,
                command=lambda m=method: self._generate_dataset(m),
            )
        
        self._create_menu_button(
            text="🔙 Tornar",
            command=self.show_main_menu,
            pady=15,
            style=styles.back_button_style
        )
    
    def show_config_menu(self):
        self._clear_frame()
        self.title("Configuració")
        
        self._create_menu_title("⚙️ Configuració de Paràmetres", pady=20)

        self._create_menu_title(
            text="Nombre de partícules:",
            style=styles.subtitle_style,
            pady=10
        )
        self.num_particules = self._create_input_box(
            self.default_dataset_config["num_particules"]
        )

        self._create_menu_title(
            text="Nombre de passos:",
            style=styles.subtitle_style,
            pady=10
        )
        self.num_passos = self._create_input_box(
            self.default_dataset_config["num_passos"]
        )

        self._create_menu_title(
            text="Paràmetres aleatoris:",
            style=styles.subtitle_style,
            pady=10
        )
        _, self.random_params = self._create_check_box(
            self.default_dataset_config["random_params"]
        )
        
        self._create_menu_button(
            "💾 Guardar Configuració",
            self._save_config,
            pady=15
        )
        
        self._create_menu_button(
            text="🔙 Tornar",
            command=self.show_generation_menu,
            pady=15,
            style=styles.back_button_style
        )
    def show_save_menu(self, dataset):
        self._clear_frame()
        self.title("Desar Dataset")

        self._create_menu_title("💾 Desar Dataset")

        self._create_menu_title(
            text = "Nom del fitxer:",
            style = styles.subtitle_style,
            pady = 10
        )
        self.file_name = self._create_input_box("dataset.pkl")

        self._create_menu_button(
            "💾 Desar",
            lambda: self.save_dataset(dataset, self.file_name.get()),
            pady=15
        )

        self._create_menu_button(
            text="🔙 Tornar",
            command=self.show_generation_menu,
            pady=15,
            style=styles.back_button_style
        )

    def save_dataset(self, dataset, dataset_name):
        if not dataset_name.endswith(".pkl"):
            dataset_name += ".pkl"
        try:
            with open(os.path.join(self.data_dir, dataset_name), "wb") as f:
                pickle.dump(dataset, f)
            self._create_menu_title(
                text="✅ Dataset guardat!",
                style=styles.subtitle_style,
                pady=10
            )
        except Exception as e:
            self._create_menu_title(
                text=f"⛔ Error: {str(e)}",
                style=styles.subtitle_style,
                pady=10
            )

    def show_load_menu(self):
        self._clear_frame()
        self.title("Carregar Dataset")

        self._create_menu_title("📂 Carregar Dataset")

        # Llistar arxius .pkl
        files = [f for f in os.listdir(self.data_dir) if f.endswith(".pkl")]
        
        if files:
            for idx, filename in enumerate(files, 1):
                self._create_menu_button(
                    text=f"{idx}. {filename}",
                    command=lambda f=filename: self.load_dataset(f),
                    style={"width": 300},
                    pady=5
                )
        else:
            self._create_menu_title(
                text="No s'han trobat datasets",
                style=styles.subtitle_style,
                pady=10
            )

        self._create_menu_button(
            text="🔙 Tornar",
            command=self.show_main_menu,
            pady=15,
            style=styles.back_button_style
        )

    def load_dataset(self, filename):
        try:
            with open(os.path.join(self.data_dir, filename), "rb") as f:
                dataset = pickle.load(f)
            self.show_analysis_menu(dataset)
        except Exception as e:
            self._create_menu_title(
                text=f"⛔ Error: {str(e)}",
                style=styles.subtitle_style,
                pady=10
            )

    def show_analysis_menu(self, dataset):
        self._clear_frame()
        self.title("Anàlisi del Dataset")

        self._create_menu_title("🔎 Anàlisi del Dataset")

        self._create_menu_button(
            "📊 Anàlisi Estadística",
            lambda: self.show_statistical_analysis(dataset),
            pady=10
        )
        self._create_menu_button(
            "🤖 Inferència amb Models",
            lambda: self.show_model_inference(dataset),
            pady=10
        )
        self._create_menu_button(
            text="🔙 Tornar",
            command=self.show_load_menu,
            pady=15,
            style=styles.back_button_style
        )
    
    def show_statistical_analysis(self, dataset):
        self._clear_frame()
        self.title("Anàlisi")

        self._create_menu_title("📊 Opcions d'Anàlisi")


        self._create_menu_button(
            "📈 Mostrar Trajectòries",
            lambda: DataAnalyzer(dataset).mostrar_trajectories()
        )

        self._create_menu_button(
            "📉 Evolució Temporal",
            lambda: DataAnalyzer(dataset).mostrar_evolucio()
        )

        self._create_menu_button(
            "📊 Histograma 3D",
            lambda: DataAnalyzer(dataset).mostrar_histograma()
        )

        self._create_menu_button(
            text="🔙 Tornar",
            command=lambda: self.show_analysis_menu(dataset)
        )

if __name__ == "__main__":
    app = TrajectoriesApp()
    app.mainloop()
    
