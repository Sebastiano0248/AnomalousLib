import unittest
import matplotlib.pyplot as plt
from anomalouslib.data.DatasetGenerator import DatasetGenerator
from anomalouslib.analysis.DataAnalyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):
    
    def setUp(self):
        generator = DatasetGenerator(num_particules=5)
        self.dataset = generator.generate_RandomWalk(num_passos=30)
        self.analyzer = DataAnalyzer(self.dataset)
    
    def test_mostrar_trajectories(self):
        plt_obj, fig, ax = self.analyzer.mostrar_trajectories(draw=False)
        self.assertIsNotNone(fig)
        plt.close(fig)
    
    def test_mostrar_evolucio(self):
        plt_obj, fig, ax = self.analyzer.mostrar_evolucio(draw=False)
        self.assertIsNotNone(fig)
        self.assertTrue(len(ax.lines) > 0)
        plt.close(fig)
    
    def test_mostrar_histograma(self):
        plt_obj, fig, ax = self.analyzer.mostrar_histograma(draw=False)
        self.assertIsNotNone(fig)
        self.assertEqual(ax.name, '3d')
        plt.close(fig)
    
    def test_different_datasets(self):
        generator = DatasetGenerator(num_particules=3)
        
        datasets = [
            generator.generate_BrownianMotion(num_passos=20),
            generator.generate_FractionalBrownianMotion(num_passos=20)
        ]
        
        for dataset in datasets:
            analyzer = DataAnalyzer(dataset)
            plt_obj, fig, ax = analyzer.mostrar_trajectories(draw=False)
            self.assertIsNotNone(fig)
            plt.close(fig)

if __name__ == "__main__":
    unittest.main()
