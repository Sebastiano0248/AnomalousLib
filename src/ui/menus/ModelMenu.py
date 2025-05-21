from src.ui.menus.Menu import Menu
from src.ui.menus.LoadMenu import LoadMenu
from src.ui.menus.SaveMenu import SaveMenu
from src.utils.helpers import load_param
from src.models.testing_utils import predict_continuous
from src.data.preprocessing import generate_tensors
from src.utils.load_save_like import load_from_pickle, save_to_csv
from src.models.model_handler import load_model
from src.ui.helpers.utils import clear_frame
from src.ui.helpers.constants import Styles
from src.analysis.DataAnalyzer import DataAnalyzer


import pandas as pd

class ModelMenu(Menu):
    def __init__(self, back_menu):
        super().__init__()

        # Variables globals
        self.back_menu = back_menu

        # Paths
        self.data_dir = load_param("path", "dataset>generated")
        self.model_dir = load_param("path", "model")

        # Objectes necessaris
        self.lm = LoadMenu()
        self.sm = SaveMenu(
            "resultat",
            lambda: self.show_results(self.model)
        )

    def show_model_menu(self):
        self.show_dataset_list()
    
    def show_dataset_list(self):
        self.lm.show_load_menu(
            "dataset", ".pkl",
            load_param("path", "dataset>generated"),
            lambda filename: load_from_pickle(self.data_dir, filename),
            self.show_analysis_menu,
            self.back_menu
        )

    def show_analysis_menu(self, dataset):
        clear_frame()
        self.app.title("Anàlisi del Dataset")

        self.ui.title("🔎 Anàlisi del Dataset")

        self.ui.button(
            "📊 Anàlisi Estadística",
            lambda: self.show_statistical_analysis(dataset),
            pady=10
        )
        self.ui.button(
            "🤖 Inferència amb Models",
            lambda: self.show_model_list(dataset),
            pady=10
        )

        self.ui.back_button(self.show_dataset_list)

    def show_statistical_analysis(self, dataset):
        clear_frame()
        self.app.title("Anàlisi")

        self.ui.title("📊 Opcions d'Anàlisi")
        da = DataAnalyzer(dataset)

        self.ui.button(
            "📈 Mostrar Trajectòries",
            lambda: da.mostrar_trajectories()
        )

        self.ui.button(
            "📉 Evolució Temporal",
            lambda: da.mostrar_evolucio()
        )

        self.ui.button(
            "📊 Histograma 3D",
            lambda: da.mostrar_histograma()
        )

        self.ui.back_button(lambda: self.show_analysis_menu(dataset))

    def show_model_list(self, dataset):
        self.dataset = dataset
        self.lm.show_load_menu(
            "model", ".pth",
            load_param("path", "model"),
            lambda filename: load_model(self.model_dir + filename),
            self.show_results,
            lambda: self.show_analysis_menu(self.dataset)
        )
    
    def show_results(self, model):
        self.model = model
        lentgh = len(self.dataset)
        x, y = generate_tensors(self.dataset, "hurst")
        results = predict_continuous(self.model, x, y, to_print=False)
        
        clear_frame()
        self.ui.title("📋 Resultats de la Inferència")
        if lentgh > 10:
            self.ui.title(
                text="Mostrant només les primeres 10 files",
                style=Styles.subtitle_style,
                pady=10
            )
            # Afegir una última fila amb punts suspensius a cada columna
            ellipsis_row = {col: "..." for col in results.columns}
            results_to_show = pd.concat([results.head(10), pd.DataFrame([ellipsis_row])], ignore_index=True)
        
        self.ui.table_for_dataframe(results_to_show, pady=20)

        self.ui.button(
            text="💾 Guardar Resultats",
            command=
                lambda: self.sm.show_save_menu(
                    lambda filename: save_to_csv(
                        results,
                        load_param("path", "result>prediction"),
                        filename
                    )
                ),
            pady=10
        )

        self.ui.back_button(lambda: self.show_model_list(self.dataset))