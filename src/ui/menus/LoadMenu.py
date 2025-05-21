from src.ui.menus.Menu import Menu
from src.ui.helpers.utils import clear_frame
from src.ui.helpers.constants import Styles

import os

class LoadMenu(Menu):
    def __init__(self):
        super().__init__()

    def show_load_menu(self, value_type_name, extension, directory, load_method, go_to, back_menu):
        clear_frame()
        self.app.title(f"Carregar {value_type_name.title()}")

        self.ui.title(f"📂 Carregar {value_type_name.title()}")

        # Llistar arxius .pkl
        files = [f for f in os.listdir(directory) if f.endswith(extension)]
        
        if files:
            for idx, filename in enumerate(files, 1):
                self.ui.button(
                    text=f"{idx}. {filename}",
                    command=lambda f=filename: self._load_value(f, load_method, go_to),
                    style={"width": 300},
                    pady=5
                )
        else:
            self.ui.title(
                text="No s'han trobat datasets",
                style=Styles.subtitle_style,
                pady=10
            )

        self.ui.back_button(back_menu)

    def _load_value(self, filename, load_method, go_to):
        try:
            value = load_method(filename)
            go_to(value)

        except Exception as e:
            self.ui.title(
                text=f"⛔ Error: {str(e)}",
                style=Styles.subtitle_style,
                pady=10
            )