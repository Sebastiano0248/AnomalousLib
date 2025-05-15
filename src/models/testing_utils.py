import torch

def evaluate_model(model, X_test, y_test):
    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test)
        _, predicted = torch.max(test_outputs, 1)
        true_labels = torch.argmax(y_test, dim=1)
        accuracy = (predicted == true_labels).float().mean()
    print(f'Test Accuracy: {accuracy.item():.4f}')
    return accuracy.item()

def predict_discrete(model, X_input, y_input=None, le=None, single_example=False):
    # Si es un solo ejemplo, añadir dimensión batch
    if single_example:
        X_input = X_input.unsqueeze(0)
        if y_input is not None:
            y_input = y_input.unsqueeze(0)

    model.eval()
    with torch.no_grad():
        output = model(X_input)
        predicted_class = torch.argmax(output, dim=1).cpu().numpy()

    print("Predicción (índice de clase):", predicted_class)
    if le is not None:
        print("Clase predicha:", le.inverse_transform(predicted_class))
    if y_input is not None and le is not None:
        true_class = torch.argmax(y_input, dim=1).cpu().numpy()
        print("Clase real:", le.inverse_transform(true_class))

def predict_continuous(model, X_input, y_input=None, single_example=False):
    # Si es un solo ejemplo, añadir dimensión batch
    if single_example:
        X_input = X_input.unsqueeze(0)
        if y_input is not None:
            y_input = y_input.unsqueeze(0)

    model.eval()
    with torch.no_grad():
        output = model(X_input)
        predicted_value = output.cpu().numpy()

    print("Predicción:", predicted_value)
    if y_input is not None:
        true_value = y_input.cpu().numpy()
        print("Valor real:", true_value)
