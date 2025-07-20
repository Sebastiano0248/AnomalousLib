import unittest
import pandas as pd
from anomalouslib.data.DatasetGenerator import DatasetGenerator

class TestDatasetGenerator(unittest.TestCase):
    
    def setUp(self):
        self.generator = DatasetGenerator(num_particules=5)
        self.num_passos = 30
    
    def test_random_walk(self):
        dataset = self.generator.generate_RandomWalk(num_passos=self.num_passos)
        self.assertEqual(len(dataset), 5)
        self.assertTrue(all(col in dataset.columns for col in ["coords", "num_steps", "attributes"]))
    
    def test_brownian_motion(self):
        dataset = self.generator.generate_BrownianMotion(num_passos=self.num_passos)
        self.assertEqual(len(dataset), 5)
        self.assertEqual(dataset.iloc[0]["attributes"]["trajectory_type"], "Brownian Motion")
    
    def test_fractional_brownian_motion(self):
        dataset = self.generator.generate_FractionalBrownianMotion(num_passos=self.num_passos)
        self.assertEqual(len(dataset), 5)
        self.assertIn("hurst", dataset.iloc[0]["attributes"])
    
    def test_all_trajectory_types(self):
        methods = [
            self.generator.generate_RandomWalk,
            self.generator.generate_BrownianMotion,
            self.generator.generate_FractionalBrownianMotion,
            self.generator.generate_ContinuousTimeRandomWalk,
            self.generator.generate_LevyWalks,
            self.generator.generate_AnnealedTransitTimeModel,
            self.generator.generate_ScaledBrownianMotion
        ]
        
        for method in methods:
            dataset = method(num_passos=20)
            self.assertEqual(len(dataset), 5)
    
    def test_random_params(self):
        dataset1 = self.generator.generate_FractionalBrownianMotion(num_passos=20, random_params=True)
        dataset2 = self.generator.generate_FractionalBrownianMotion(num_passos=20, random_params=True)
        
        hurst1 = dataset1.iloc[0]["attributes"]["hurst"]
        hurst2 = dataset2.iloc[0]["attributes"]["hurst"]
        self.assertNotEqual(hurst1, hurst2)

if __name__ == "__main__":
    unittest.main()
