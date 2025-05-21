from customtkinter import CTkFrame, CTkButton
# from controllers.trajectories_controller import TrajectoryController

class SimulationTab(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # self.controller = TrajectoryController()

        CTkButton(self, text="Simular", command=self.simular).pack(pady=10)

    def simular(self):
        resultado = self.controller.simulate_trajectory()
        print("Resultado:", resultado)