import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import DataLoader, TensorDataset
import torch
import dill
import pickle

def load_dynamic_model(model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(model_path, map_location=device, pickle_module=dill)
    
    # Ejecutar el código fuente para recrear la clase
    exec(checkpoint["model_source"], globals())  # La clase se define en el scope global
    
    # Instanciar el modelo con sus argumentos originales
    model_class = globals()[checkpoint["model_source"].split("class ")[1].split("(")[0].strip()]
    model = model_class(**checkpoint["attributes"])
    model.load_state_dict(checkpoint["state_dict"])
    model.to(device)
    model.eval()
    return model

# Uso
model = load_dynamic_model("model.pth")
print(model)  # Muestra la estructura del modelo cargado


with open('../../data/generated/all_types_200p_70000t_rp.pkl', 'rb') as file:
    data = pickle.load(file)

data = data.sample(frac=1).reset_index(drop=True)

valores_unicos = data['trajectory_type'].unique()
coords_list = [np.stack([row[0], row[1]], axis=1) for row in data['coords']]
X = np.array(coords_list)  # Forma (n_samples, seq_length, 2)
X_tensor = torch.tensor(X, dtype=torch.float32)
le = LabelEncoder()
labels = le.fit_transform(data['trajectory_type'])
labels_tensor  = torch.tensor(labels, dtype=torch.long)
y_tensor = F.one_hot(labels_tensor, num_classes=7).float()
X_tensor = X_tensor.permute(0, 2, 1)  # Nueva forma: (n, 2, m)
train_size = int(0.8 * len(X_tensor))
X_train, X_test = X_tensor[:train_size], X_tensor[train_size:]
y_train, y_test = y_tensor[:train_size], y_tensor[train_size:]



# Seleccionar el primer ejemplo de X_test y añadir una dimensión batch
first_example = X_test[0].unsqueeze(0)  # shape: (1, 2, 200)

# Pasar por el modelo
model.eval()
with torch.no_grad():
    output = model(first_example)
    predicted_class = torch.argmax(output, dim=1).item()

# Mostrar el resultado
print("Predicción (índice de clase):", predicted_class)
print("Clase predicha:", le.inverse_transform([predicted_class])[0])
# Mostrar la clase real
true_class = torch.argmax(y_test[0]).item()
print("Clase real:", le.inverse_transform([true_class])[0])