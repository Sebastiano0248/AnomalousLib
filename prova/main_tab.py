from customtkinter import CTkFrame, CTkLabel

class MainTab(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        CTkLabel(self, text="Bienvenido a la app de trayectorias").pack(pady=20)