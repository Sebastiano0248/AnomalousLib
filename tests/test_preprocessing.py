import unittest
import torch
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from anomalouslib.data.DatasetGenerator import DatasetGenerator
from anomalouslib.data.preprocessing import (
    generate_regressor_tensors, 
    generate_classification_tensors,
    min_max_normalize
)
from anomalouslib.data.postprocessing import min_max_denormalize

class TestPreprocessing(unittest.TestCase):
    
    def setUp(self):
        generator = DatasetGenerator(num_particules=10)
        self.fbm_dataset = generator.generate_FractionalBrownianMotion(num_passos=30, random_params=True)
        
        rw_data = generator.generate_RandomWalk(num_passos=30)
        bm_data = generator.generate_BrownianMotion(num_passos=30)
        self.mixed_dataset = pd.concat([self.fbm_dataset, bm_data, rw_data], ignore_index=True)
    
    def test_min_max_normalize(self):
        normalized = min_max_normalize(0.5, 0.0, 1.0)
        self.assertEqual(normalized, 0.5)
        
        normalized = min_max_normalize(75, 50, 100)
        self.assertEqual(normalized, 0.5)
    
    def test_min_max_denormalize(self):
        denormalized = min_max_denormalize(0.5, 0.0, 1.0)
        self.assertEqual(denormalized, 0.5)
        
        original = 75
        normalized = min_max_normalize(original, 50, 100)
        denormalized = min_max_denormalize(normalized, 50, 100)
        self.assertAlmostEqual(denormalized, original, places=10)
    
    def test_generate_regressor_tensors(self):
        X_tensor, y_tensor = generate_regressor_tensors(
            self.fbm_dataset, "Fractional Brownian Motion", "hurst"
        )
        
        self.assertEqual(X_tensor.shape[0], 10)
        self.assertEqual(X_tensor.shape[1], 2)
        self.assertEqual(y_tensor.shape[0], 10)
        self.assertEqual(y_tensor.shape[1], 1)
        self.assertTrue(torch.all(y_tensor >= 0) and torch.all(y_tensor <= 1))
    
    def test_generate_classification_tensors(self):
        le = LabelEncoder()
        trajectory_types = self.mixed_dataset["attributes"].apply(lambda x: x["trajectory_type"])
        le.fit(trajectory_types)
        
        X_tensor, y_tensor = generate_classification_tensors(
            self.mixed_dataset, "trajectory_type", le
        )
        
        self.assertEqual(X_tensor.shape[0], len(self.mixed_dataset))
        self.assertEqual(X_tensor.shape[1], 2)
        self.assertEqual(y_tensor.shape[1], 7)
        self.assertTrue(torch.all(torch.sum(y_tensor, dim=1) == 1))

if __name__ == "__main__":
    unittest.main()
