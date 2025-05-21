from customtkinter import CTk, CTkTabview
from main_tab import MainTab
from simulation_tab import SimulationTab

class TrajectoriesApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("Trajectory App")
        self.geometry("800x600")

        self.tabview = CTkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        # Pestañas
        self.main_tab = MainTab(self.tabview)
        self.simulation_tab = SimulationTab(self.tabview)

        self.tabview.add("Principal")
        self.tabview.add("Simulación")

        self.main_tab.pack(in_=self.tabview.tab("Principal"), fill="both", expand=True)
        self.simulation_tab.pack(in_=self.tabview.tab("Simulación"), fill="both", expand=True)

app = TrajectoriesApp()
app.mainloop()