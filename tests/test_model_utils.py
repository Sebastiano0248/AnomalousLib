import unittest
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import LabelEncoder
from anomalouslib.data.DatasetGenerator import DatasetGenerator
from anomalouslib.data.preprocessing import generate_regressor_tensors, generate_classification_tensors
from anomalouslib.models.training_utils import train_model
from anomalouslib.models.testing_utils import evaluate_discrete, evaluate_continuous, predict_continuous

class SimpleModel(nn.Module):
    def __init__(self, output_size=1):
        super().__init__()
        self.conv = nn.Conv1d(2, 8, kernel_size=3, padding=1)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(8, output_size)
    
    def forward(self, x):
        x = torch.relu(self.conv(x))
        x = self.pool(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

class TestModelUtils(unittest.TestCase):
    
    def setUp(self):
        generator = DatasetGenerator(num_particules=20)
        self.fbm_dataset = generator.generate_FractionalBrownianMotion(num_passos=30, random_params=True)
        self.X_reg, self.y_reg = generate_regressor_tensors(
            self.fbm_dataset, "Fractional Brownian Motion", "hurst"
        )
    
    def test_train_model_basic(self):
        model = SimpleModel(output_size=1)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        dataset = TensorDataset(self.X_reg, self.y_reg)
        train_loader = DataLoader(dataset, batch_size=4, shuffle=True)
        
        trained_model = train_model(
            model, train_loader, criterion, optimizer, 
            num_epochs=2, print_epoch=False
        )
        
        self.assertIsNotNone(trained_model)
    
    def test_evaluate_continuous(self):
        model = SimpleModel(output_size=1)
        mse = evaluate_continuous(model, self.X_reg[:5], self.y_reg[:5])
        self.assertIsInstance(mse, float)
        self.assertGreaterEqual(mse, 0)
    
    def test_predict_continuous(self):
        model = SimpleModel(output_size=1)
        result_df = predict_continuous(model, self.X_reg[:3], to_print=False)
        self.assertEqual(len(result_df), 3)
        self.assertIn('Prediction', result_df.columns)
    
    def test_train_with_validation(self):
        model = SimpleModel(output_size=1)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        
        split_idx = len(self.X_reg) // 2
        X_train, X_val = self.X_reg[:split_idx], self.X_reg[split_idx:]
        y_train, y_val = self.y_reg[:split_idx], self.y_reg[split_idx:]
        
        train_dataset = TensorDataset(X_train, y_train)
        val_dataset = TensorDataset(X_val, y_val)
        
        train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)
        
        trained_model = train_model(
            model, train_loader, criterion, optimizer,
            num_epochs=2, val_loader=val_loader, print_epoch=False
        )
        
        self.assertIsNotNone(trained_model)

if __name__ == "__main__":
    unittest.main()
