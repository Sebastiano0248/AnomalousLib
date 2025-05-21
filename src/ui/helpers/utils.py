from src.ui.menus.App import App

def clear_frame():
    for widget in App().main_frame.winfo_children():
        widget.destroy()