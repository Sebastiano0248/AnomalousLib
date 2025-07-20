import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestIntegration(unittest.TestCase):
    
    def test_library_imports(self):
        from anomalouslib.data.DatasetGenerator import DatasetGenerator
        from anomalouslib.analysis.DataAnalyzer import DataAnalyzer
        from anomalouslib.data.preprocessing import generate_regressor_tensors
        from anomalouslib.utils.load_save_like import save_to_pickle
        from anomalouslib.results.results import ResultManager
        from anomalouslib.constants import params
    
    def test_basic_workflow(self):
        from anomalouslib.data.DatasetGenerator import DatasetGenerator
        from anomalouslib.analysis.DataAnalyzer import DataAnalyzer
        from anomalouslib.data.preprocessing import generate_regressor_tensors
        
        generator = DatasetGenerator(num_particules=5)
        dataset = generator.generate_FractionalBrownianMotion(num_passos=30)
        
        analyzer = DataAnalyzer(dataset)
        plt_obj, fig, ax = analyzer.mostrar_trajectories(draw=False)
        plt_obj.close(fig)
        
        X_tensor, y_tensor = generate_regressor_tensors(
            dataset, "Fractional Brownian Motion", "hurst"
        )
        
        self.assertEqual(len(dataset), 5)
        self.assertEqual(X_tensor.shape[0], 5)
    
    def test_all_trajectory_types(self):
        from anomalouslib.data.DatasetGenerator import DatasetGenerator
        
        generator = DatasetGenerator(num_particules=3)
        methods = [
            generator.generate_RandomWalk,
            generator.generate_BrownianMotion,
            generator.generate_FractionalBrownianMotion,
            generator.generate_ContinuousTimeRandomWalk,
            generator.generate_LevyWalks,
            generator.generate_AnnealedTransitTimeModel,
            generator.generate_ScaledBrownianMotion
        ]
        
        for method in methods:
            dataset = method(num_passos=20)
            self.assertEqual(len(dataset), 3)

if __name__ == "__main__":
    unittest.main()
