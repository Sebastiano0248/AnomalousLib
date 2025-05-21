from src.ui.helpers.constants import Styles
from src.ui.helpers.utils import clear_frame
from src.ui.menus.Menu import Menu
from src.ui.helpers.constants import Styles

class SaveMenu(Menu):
    def __init__(self, value_type_name, back_menu):
        super().__init__()
        self.value_type_name = value_type_name
        self.back_menu = back_menu

    def show_save_menu(self, save_method):
        clear_frame()
        self.app.title(f"Desar {self.value_type_name.title()}")

        self.ui.title(f"💾 Desar {self.value_type_name.title()}")

        self.ui.title(
            text = "Nom del fitxer:",
            style = Styles.subtitle_style,
            pady = 10
        )
        self.file_name = self.ui.input_box(self.value_type_name)

        self.ui.button(
            "💾 Desar",
            lambda: self._save_in_a_file(save_method, self.file_name.get()),
            pady=15
        )

        self.ui.back_button(self.back_menu)
    
    def _save_in_a_file(self, save_method, file_name):
        try:
            save_method(file_name)

            self.ui.title(
                text=f"✅ {self.value_type_name.title()} guardat!",
                style=Styles.subtitle_style,
                pady=10
            )
        except Exception as e:
            self.ui.title(
                text=f"⛔ Error: {str(e)}",
                style=Styles.subtitle_style,
                pady=10
            )