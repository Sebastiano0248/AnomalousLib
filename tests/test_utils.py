import unittest
import os
import tempfile
import shutil
import torch
import torch.nn as nn
from anomalouslib.models.model_handler import save_model, load_model
from anomalouslib.utils.load_save_like import save_to_pickle, load_from_pickle, save_to_csv, load_from_csv
from anomalouslib.results.results import ResultManager
import pandas as pd

class TestModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(2, 1)
    
    def forward(self, x):
        return self.fc(x)

class TestUtils(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.temp_dir)
        self.test_data = {"key1": "value1", "key2": [1, 2, 3]}
        self.test_df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    
    def test_save_load_pickle(self):
        save_to_pickle(self.test_data, self.temp_dir, "test")
        loaded_data = load_from_pickle(self.temp_dir, "test.pkl")
        self.assertEqual(loaded_data, self.test_data)
    
    def test_save_load_csv(self):
        save_to_csv(self.test_df, self.temp_dir, "test")
        loaded_df = load_from_csv(self.temp_dir, "test")
        pd.testing.assert_frame_equal(loaded_df, self.test_df)
    
    def test_save_load_model(self):
        model = TestModel()
        model_source = "class TestModel(nn.Module):\n    def __init__(self):\n        super().__init__()\n        self.fc = nn.Linear(2, 1)"
        
        save_model(
            model_instance=model,
            model_type="test",
            model_source=model_source,
            params={},
            input_channels=2,
            model_name="test_model",
            path=self.temp_dir
        )
        
        model_path = os.path.join(self.temp_dir, "test_model.pth")
        self.assertTrue(os.path.exists(model_path))
        
        # Només verificar que el fitxer es pot carregar sense error
        loaded_model = load_model(model_path)
        self.assertIsNotNone(loaded_model)
    
    def test_result_manager(self):
        rm = ResultManager()
        rm.add_result("test_metric", 0.95)
        rm.add_result("data", {"size": 100})
        
        self.assertEqual(rm.results["test_metric"], 0.95)
        self.assertEqual(len(rm.results), 2)
        
        save_path = os.path.join(self.temp_dir, "results.pkl")
        rm.save_results(save_path, format="pickle")
        self.assertTrue(os.path.exists(save_path))

if __name__ == "__main__":
    unittest.main()
