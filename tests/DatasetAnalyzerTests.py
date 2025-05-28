from anomalouslib.data.DatasetGenerator import DatasetGenerator
from anomalouslib.analysis.DataAnalyzer import DataAnalyzer

try:
    print("Testing DatasetAnalyzer...")

    dg = DatasetGenerator(num_particules=30)
    dataset = dg.generate_RandomWalk(num_passos=100, random_params=True)
    da = DataAnalyzer(dataset)
    plt, fig, ax = da.mostrar_trajectories(draw=False)
    input("Pulse enter para continuar...")
    plt.show()
    da.mostrar_evolucio()
    da.mostrar_histograma()
except Exception as e:
    print(f"An error occurred during the test: {e}")
else:
    print("DatasetAnalyzer test completed successfully.")