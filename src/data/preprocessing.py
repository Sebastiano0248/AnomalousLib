from sklearn.preprocessing import LabelEncoder
import torch.nn.functional as F
import pandas as pd
import numpy as np
import torch

def min_max_normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)

def generate_regression_tensors(dataframe, parm_to_eval: str):
    # Aconseguim un dataframe amb les coordenades i la hurst
    df = dataframe[["coords", "attributes"]].copy()
    df[parm_to_eval] = df["attributes"].apply(lambda x: x[parm_to_eval])
    df = df[["coords", parm_to_eval]]

    # Tractem les coordenades per aconseguir X_tensor
    coords_list = [np.stack([row[0], row[1]], axis=1) for row in df['coords']]
    X = np.array(coords_list)  # Forma (n_samples, seq_length, 2)
    # Per aconseguir la forma (n_samples, 2, seq_length)
    X_tensor = torch.tensor(X, dtype=torch.float32).permute(0, 2, 1)

    # Tractem les coordenades per aconseguir y_tensor
    max_hurst, min_hurst = 0.9, 0.1
    hurst_series = df[parm_to_eval].apply(lambda x: min_max_normalize(x, min_hurst, max_hurst))
    labels = hurst_series.values  # Suponiendo que 'hurst' contiene los valores reales
    y_tensor = torch.tensor(labels, dtype=torch.float32).unsqueeze(1)

    return X_tensor, y_tensor

def generate_classification_tensors(dataframe, parm_to_eval: str, le = LabelEncoder()):
    # dataframe = dataframe.drop(columns=['num_steps', 'attributes'])
    dataframe = dataframe.sample(frac=1).reset_index(drop=True)

    # Tractem les coordenades per aconseguir X_tensor
    coords_list = [np.stack([row[0], row[1]], axis=1) for row in dataframe['coords']]
    X = np.array(coords_list)  # Forma (n_samples, seq_length, 2)
    X_tensor = torch.tensor(X, dtype=torch.float32).permute(0, 2, 1)

    # Tractem les coordenades per aconseguir y_tensor
    labels = le.fit_transform(dataframe[parm_to_eval])
    labels_tensor  = torch.tensor(labels, dtype=torch.long)
    y_tensor = F.one_hot(labels_tensor, num_classes=7).float()

    return X_tensor, y_tensor
